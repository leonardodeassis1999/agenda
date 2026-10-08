// Tela de Perfil: ver e editar nome e e-mail.
exigirLogin();
montarMenu("perfil.html");

const form = document.getElementById("form-perfil");
const campoNome = document.getElementById("nome");
const campoEmail = document.getElementById("email");
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

async function carregar() {
  try {
    const usuario = await api("/usuarios/me");
    campoNome.value = usuario.nome;
    campoEmail.value = usuario.email;
  } catch (erro) {
    mostrarErro(erro.message);
  }
}

form.addEventListener("submit", async (evento) => {
  evento.preventDefault();
  const botao = form.querySelector("button[type=submit]");
  botao.disabled = true;
  try {
    const usuario = await api("/usuarios/me", {
      metodo: "PUT",
      corpo: { nome: campoNome.value, email: campoEmail.value },
    });
    campoNome.value = usuario.nome;
    campoEmail.value = usuario.email;
    mostrarOk("Dados atualizados.");
  } catch (erro) {
    mostrarErro(erro.message);
  }
  botao.disabled = false;
});

document.getElementById("btn-sair").addEventListener("click", sair);
carregar();