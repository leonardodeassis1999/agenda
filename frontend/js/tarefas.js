// Tela Minhas tarefas: lista com filtros.
exigirLogin();
montarMenu("tarefas.html");

const fStatus = document.getElementById("f-status");
const fData = document.getElementById("f-data");
const fAtrasadas = document.getElementById("f-atrasadas");
const lista = document.getElementById("lista");
const contagem = document.getElementById("contagem");
const caixaErro = document.getElementById("erro");

async function carregar() {
  const params = new URLSearchParams();
  if (fStatus.value) params.set("status", fStatus.value);
  if (fData.value) params.set("data", fData.value);
  if (fAtrasadas.checked) params.set("atrasadas", "true");
  const consulta = params.toString();

  try {
    const tarefas = await api("/tarefas" + (consulta ? "?" + consulta : ""));
    caixaErro.hidden = true;
    mostrar(tarefas);
  } catch (erro) {
    caixaErro.textContent = erro.message;
    caixaErro.hidden = false;
  }
}

function mostrar(tarefas) {
  lista.replaceChildren();
  const minutos = tarefas.reduce((soma, t) => soma + t.tempo_estimado_min, 0);
  contagem.textContent = tarefas.length
    ? `${tarefas.length} tarefa(s) · ${formatarTempo(minutos)} no total`
    : "";

  if (tarefas.length === 0) {
    const vazio = el("div", "vazio", "Nenhuma tarefa encontrada. ");
    const link = el("a", "", "Criar uma tarefa");
    link.href = "tarefa.html";
    vazio.appendChild(link);
    lista.appendChild(vazio);
    return;
  }
  for (const t of tarefas) {
    lista.appendChild(criarCartaoTarefa(t, acoesDaTarefa(t, carregar)));
  }
}

fStatus.addEventListener("change", carregar);
fData.addEventListener("change", carregar);
fAtrasadas.addEventListener("change", carregar);
document.getElementById("f-limpar").addEventListener("click", () => {
  fStatus.value = "";
  fData.value = "";
  fAtrasadas.checked = false;
  carregar();
});

carregar();