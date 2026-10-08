// Tela Nova / Editar tarefa. Com ?id=5 na URL, edita a tarefa 5.
exigirLogin();
montarMenu("tarefa.html");

const idTarefa = new URLSearchParams(window.location.search).get("id");

const form = document.getElementById("form-tarefa");
const campos = {
  titulo: document.getElementById("titulo"),
  descricao: document.getElementById("descricao"),
  categoria: document.getElementById("categoria"),
  prioridade: document.getElementById("prioridade"),
  data: document.getElementById("data"),
  tempo: document.getElementById("tempo"),
};
const btnSalvar = document.getElementById("btn-salvar");
const btnOutra = document.getElementById("btn-outra");
const btnExcluir = document.getElementById("btn-excluir");
const caixaErro = document.getElementById("erro");
const caixaOk = document.getElementById("ok");

function mostrarErro(texto) {
  caixaOk.hidden = true;
  caixaErro.textContent = texto;
  caixaErro.hidden = false;
}

function mostrarOk(texto) {
  caixaErro.hidden = true;
  caixaOk.textContent = texto;
  caixaOk.hidden = false;
}

function travar(travado) {
  btnSalvar.disabled = travado;
  btnOutra.disabled = travado;
  btnExcluir.disabled = travado;
}

// Atalhos de tempo
document.getElementById("chips").addEventListener("click", (evento) => {
  const minutos = evento.target.dataset.min;
  if (minutos) campos.tempo.value = minutos;
});

// Sugestões de categoria: as que o usuário já usou
async function carregarCategorias() {
  try {
    const tarefas = await api("/tarefas");
    const usadas = [...new Set(tarefas.map((t) => t.categoria).filter(Boolean))];
    const lista = document.getElementById("categorias");
    for (const nome of usadas) {
      const opcao = document.createElement("option");
      opcao.value = nome;
      lista.appendChild(opcao);
    }
  } catch (e) {}
}

async function carregarTarefa() {
  try {
    const t = await api(`/tarefas/${idTarefa}`);
    campos.titulo.value = t.titulo;
    campos.descricao.value = t.descricao || "";
    campos.categoria.value = t.categoria || "";
    campos.prioridade.value = t.prioridade;
    campos.data.value = t.data_prevista;
    campos.tempo.value = t.tempo_estimado_min;
  } catch (erro) {
    form.hidden = true;
    mostrarErro(erro.message);
  }
}

function lerCorpo() {
  return {
    titulo: campos.titulo.value,
    descricao: campos.descricao.value.trim() || null,
    categoria: campos.categoria.value.trim() || null,
    prioridade: campos.prioridade.value,
    data_prevista: campos.data.value,
    tempo_estimado_min: Number(campos.tempo.value),
  };
}

async function salvar(criarOutra) {
  if (!form.reportValidity()) return;
  caixaErro.hidden = true;
  caixaOk.hidden = true;
  travar(true);
  try {
    const corpo = lerCorpo();
    if (idTarefa) {
      await api(`/tarefas/${idTarefa}`, { metodo: "PUT", corpo });
    } else {
      await api("/tarefas", { metodo: "POST", corpo });
    }
    if (criarOutra) {
      campos.titulo.value = "";
      campos.descricao.value = "";
      mostrarOk("Tarefa salva. Pode cadastrar a próxima.");
      campos.titulo.focus();
    } else {
      window.location.href = corpo.data_prevista === hojeISO() ? "meu-dia.html" : "tarefas.html";
      return;
    }
  } catch (erro) {
    mostrarErro(erro.message);
  }
  travar(false);
}

form.addEventListener("submit", (evento) => {
  evento.preventDefault();
  salvar(false);
});
btnOutra.addEventListener("click", () => salvar(true));

btnExcluir.addEventListener("click", async () => {
  if (!confirm("Excluir esta tarefa? Isso não pode ser desfeito.")) return;
  travar(true);
  try {
    await api(`/tarefas/${idTarefa}`, { metodo: "DELETE" });
    window.location.href = "tarefas.html";
  } catch (erro) {
    mostrarErro(erro.message);
    travar(false);
  }
});

// Início
campos.data.value = hojeISO();
carregarCategorias();
if (idTarefa) {
  document.getElementById("titulo-pagina").textContent = "Editar tarefa";
  btnOutra.hidden = true;
  btnExcluir.hidden = false;
  carregarTarefa();
}