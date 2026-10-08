// Funções usadas por todas as telas: token e chamadas à API.
const TOKEN_KEY = "meudia_token";
const PAGINA_LOGIN = "index.html";
const PAGINA_INICIAL = "meu-dia.html"; // criada em um passo futuro

function salvarToken(token) {
  localStorage.setItem(TOKEN_KEY, token);
}

function lerToken() {
  return localStorage.getItem(TOKEN_KEY);
}

function sair() {
  localStorage.removeItem(TOKEN_KEY);
  window.location.href = PAGINA_LOGIN;
}

// Telas protegidas chamam esta função no início.
function exigirLogin() {
  if (!lerToken()) window.location.href = PAGINA_LOGIN;
}

function mensagemDeErro(corpo) {
  if (!corpo || !corpo.detail) return "Algo deu errado. Tente novamente.";
  if (typeof corpo.detail === "string") return corpo.detail;
  if (Array.isArray(corpo.detail)) {
    const campos = corpo.detail.map((e) => e.loc[e.loc.length - 1]);
    return "Confira os campos: " + [...new Set(campos)].join(", ") + ".";
  }
  return "Algo deu errado. Tente novamente.";
}

// Faz a chamada à API. Em caso de erro, lança Error com a mensagem para o usuário.
async function api(caminho, { metodo = "GET", corpo = null } = {}) {
  const cabecalhos = {};
  if (corpo !== null) cabecalhos["Content-Type"] = "application/json";
  const token = lerToken();
  if (token) cabecalhos["Authorization"] = "Bearer " + token;

  let resposta;
  try {
    resposta = await fetch(caminho, {
      method: metodo,
      headers: cabecalhos,
      body: corpo !== null ? JSON.stringify(corpo) : null,
    });
  } catch (e) {
    throw new Error("Sem conexão com o servidor.");
  }

  // Token vencido ou inválido: volta para o login (exceto nas rotas /auth).
  if (resposta.status === 401 && !caminho.startsWith("/auth")) {
    sair();
    throw new Error("Sessão expirada. Entre novamente.");
  }

  if (resposta.status === 204) return null;

  let dados = null;
  try {
    dados = await resposta.json();
  } catch (e) {}

  if (!resposta.ok) throw new Error(mensagemDeErro(dados));
  return dados;
}