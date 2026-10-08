// Tela Meu Dia: tarefas de hoje, atrasadas e progresso.
exigirLogin();
montarMenu("meu-dia.html");

const ORDEM_STATUS = { em_andamento: 0, pendente: 1, concluida: 2 };
const ORDEM_PRIORIDADE = { alta: 0, media: 1, baixa: 2 };

const caixaErro = document.getElementById("erro");

function ordenar(tarefas) {
  return [...tarefas].sort(
    (a, b) =>
      ORDEM_STATUS[a.status] - ORDEM_STATUS[b.status] ||
      ORDEM_PRIORIDADE[a.prioridade] - ORDEM_PRIORIDADE[b.prioridade] ||
      a.tempo_estimado_min - b.tempo_estimado_min
  );
}

function itemResumo(valor, rotulo) {
  const item = el("div", "resumo-item");
  item.appendChild(el("span", "resumo-valor", valor));
  item.appendChild(el("span", "resumo-rotulo", rotulo));
  return item;
}

function mostrarResumo(hoje) {
  const total = hoje.length;
  const concluidas = hoje.filter((t) => t.status === "concluida").length;
  const minutos = hoje.reduce((soma, t) => soma + t.tempo_estimado_min, 0);
  const altas = hoje.filter((t) => t.prioridade === "alta");
  const altasFeitas = altas.filter((t) => t.status === "concluida").length;
  const percentual = total ? Math.round((concluidas / total) * 100) : 0;

  document.getElementById("barra").style.width = percentual + "%";
  const resumo = document.getElementById("resumo");
  resumo.replaceChildren(
    itemResumo(`${percentual}%`, "do dia concluído"),
    itemResumo(`${concluidas}/${total}`, "tarefas concluídas"),
    itemResumo(formatarTempo(minutos), "tempo planejado")
  );
  if (altas.length) {
    resumo.appendChild(itemResumo(`${altasFeitas}/${altas.length}`, "prioridades altas"));
  }
}

function mostrarHoje(hoje) {
  const lista = document.getElementById("lista-hoje");
  lista.replaceChildren();
  if (hoje.length === 0) {
    const vazio = el("div", "vazio", "Nenhuma tarefa para hoje. ");
    const link = el("a", "", "Planejar o dia");
    link.href = "tarefa.html";
    vazio.appendChild(link);
    lista.appendChild(vazio);
    return;
  }
  for (const t of ordenar(hoje)) {
    lista.appendChild(criarCartaoTarefa(t, acoesDaTarefa(t, carregar)));
  }
}

function mostrarAtrasadas(atrasadas) {
  const secao = document.getElementById("sec-atrasadas");
  const lista = document.getElementById("lista-atrasadas");
  lista.replaceChildren();
  secao.hidden = atrasadas.length === 0;
  document.getElementById("titulo-atrasadas").textContent = `Atrasadas (${atrasadas.length})`;

  for (const t of ordenar(atrasadas)) {
    const acoes = acoesDaTarefa(t, carregar);
    acoes.unshift({
      texto: "Mover para hoje",
      classe: "btn",
      fn: () =>
        executar(
          () => api(`/tarefas/${t.id}`, { metodo: "PUT", corpo: { data_prevista: hojeISO() } }),
          carregar
        ),
    });
    lista.appendChild(criarCartaoTarefa(t, acoes));
  }
}

async function carregar() {
  try {
    const [hoje, atrasadas] = await Promise.all([
      api("/tarefas?data=" + hojeISO()),
      api("/tarefas?atrasadas=true"),
    ]);
    caixaErro.hidden = true;
    mostrarResumo(hoje);
    mostrarHoje(hoje);
    mostrarAtrasadas(atrasadas);
  } catch (erro) {
    caixaErro.textContent = erro.message;
    caixaErro.hidden = false;
  }
}

async function iniciar() {
  document.getElementById("data-hoje").textContent = new Date().toLocaleDateString("pt-BR", {
    weekday: "long", day: "numeric", month: "long",
  });
  try {
    const usuario = await api("/usuarios/me");
    document.getElementById("saudacao").textContent = "Olá, " + usuario.nome + "!";
  } catch (e) {}
  carregar();
}

iniciar();