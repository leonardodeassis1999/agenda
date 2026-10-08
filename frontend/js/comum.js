// Funções comuns às telas de tarefas.
const PRIORIDADES = { alta: "Alta", media: "Média", baixa: "Baixa" };
const STATUS = { pendente: "Pendente", em_andamento: "Em andamento", concluida: "Concluída" };

function hojeISO() {
  const d = new Date();
  const mes = String(d.getMonth() + 1).padStart(2, "0");
  const dia = String(d.getDate()).padStart(2, "0");
  return d.getFullYear() + "-" + mes + "-" + dia;
}

function formatarData(iso) {
  const [a, m, d] = iso.split("-");
  return d + "/" + m + "/" + a;
}

function formatarTempo(min) {
  const h = Math.floor(min / 60);
  const m = min % 60;
  if (h === 0) return m + " min";
  if (m === 0) return h + " h";
  return h + "h" + String(m).padStart(2, "0");
}

function el(tag, classe, texto) {
  const e = document.createElement(tag);
  if (classe) e.className = classe;
  if (texto !== undefined) e.textContent = texto;
  return e;
}

// Executa uma ação da tarefa, avisa se der erro e recarrega a lista.
async function executar(acao, recarregar) {
  try {
    await acao();
  } catch (erro) {
    alert(erro.message);
  }
  await recarregar();
}

// Ações padrão: começar, concluir, editar e excluir.
function acoesDaTarefa(t, recarregar) {
  const acoes = [];
  if (t.status === "pendente") {
    acoes.push({
      texto: "Começar", classe: "btn",
      fn: () => executar(() => api(`/tarefas/${t.id}/iniciar`, { metodo: "POST" }), recarregar),
    });
  }
  if (t.status !== "concluida") {
    acoes.push({
      texto: "Concluir", classe: "btn btn-primario",
      fn: () => executar(() => api(`/tarefas/${t.id}/concluir`, { metodo: "POST" }), recarregar),
    });
  }
  acoes.push({ texto: "Editar", classe: "btn", href: `tarefa.html?id=${t.id}` });
  acoes.push({
    texto: "Excluir", classe: "btn btn-perigo",
    fn: () => {
      if (!confirm(`Excluir "${t.titulo}"? Isso não pode ser desfeito.`)) return;
      executar(() => api(`/tarefas/${t.id}`, { metodo: "DELETE" }), recarregar);
    },
  });
  return acoes;
}

function criarCartaoTarefa(t, acoes) {
  const cartao = el("article", `tarefa prioridade-${t.prioridade} status-${t.status}`);

  const topo = el("div", "tarefa-topo");
  topo.appendChild(el("h3", "tarefa-titulo", t.titulo));
  const selos = el("div", "selos");
  selos.appendChild(el("span", "selo", PRIORIDADES[t.prioridade]));
  if (t.atrasada) selos.appendChild(el("span", "selo selo-atrasada", "Atrasada"));
  if (t.status !== "pendente") {
    selos.appendChild(el("span", `selo selo-${t.status}`, STATUS[t.status]));
  }
  topo.appendChild(selos);
  cartao.appendChild(topo);

  const partes = [formatarData(t.data_prevista), formatarTempo(t.tempo_estimado_min)];
  if (t.categoria) partes.push(t.categoria);
  cartao.appendChild(el("p", "tarefa-meta", partes.join(" · ")));
  if (t.descricao) cartao.appendChild(el("p", "tarefa-desc", t.descricao));

  const barra = el("div", "acoes");
  for (const a of acoes) {
    let item;
    if (a.href) {
      item = el("a", a.classe, a.texto);
      item.href = a.href;
    } else {
      item = el("button", a.classe, a.texto);
      item.type = "button";
      item.addEventListener("click", a.fn);
    }
    barra.appendChild(item);
  }
  cartao.appendChild(barra);
  return cartao;
}