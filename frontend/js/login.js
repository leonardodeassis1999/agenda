// Tela de Login / Cadastro.
if (lerToken()) window.location.href = PAGINA_INICIAL;

const formEntrar = document.getElementById("form-entrar");
const formCadastro = document.getElementById("form-cadastro");
const abaEntrar = document.getElementById("aba-entrar");
const abaCadastro = document.getElementById("aba-cadastro");
const caixaMensagem = document.getElementById("mensagem");

function mostrarMensagem(texto) {
  caixaMensagem.textContent = texto; // textContent: nunca insere HTML
  caixaMensagem.hidden = false;
}

function esconderMensagem() {
  caixaMensagem.hidden = true;
}

function trocarAba(entrar) {
  formEntrar.hidden = !entrar;
  formCadastro.hidden = entrar;
  abaEntrar.classList.toggle("ativa", entrar);
  abaCadastro.classList.toggle("ativa", !entrar);
  esconderMensagem();
}

abaEntrar.addEventListener("click", () => trocarAba(true));
abaCadastro.addEventListener("click", () => trocarAba(false));

async function entrar(email, senha) {
  const dados = await api("/auth/login", {
    metodo: "POST",
    corpo: { email, senha },
  });
  salvarToken(dados.access_token);
  window.location.href = PAGINA_INICIAL;
}

// Roda a ação e desabilita o botão enquanto espera.
async function enviar(formulario, acao) {
  esconderMensagem();
  const botao = formulario.querySelector("button[type=submit]");
  botao.disabled = true;
  try {
    await acao();
  } catch (erro) {
    mostrarMensagem(erro.message);
    botao.disabled = false;
  }
}

formEntrar.addEventListener("submit", (evento) => {
  evento.preventDefault();
  enviar(formEntrar, () =>
    entrar(
      document.getElementById("login-email").value,
      document.getElementById("login-senha").value
    )
  );
});

formCadastro.addEventListener("submit", (evento) => {
  evento.preventDefault();
  enviar(formCadastro, async () => {
    const email = document.getElementById("cad-email").value;
    const senha = document.getElementById("cad-senha").value;
    await api("/auth/cadastro", {
      metodo: "POST",
      corpo: {
        nome: document.getElementById("cad-nome").value,
        email,
        senha,
      },
    });
    await entrar(email, senha); // já entra depois de criar a conta
  });
});