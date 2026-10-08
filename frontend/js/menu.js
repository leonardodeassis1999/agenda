// Menu de navegação das telas internas. Cada tela chama montarMenu("nome-da-pagina").
function montarMenu(atual) {
  const itens = [
    ["meu-dia.html", "Meu Dia"],
    ["tarefas.html", "Minhas tarefas"],
    ["tarefa.html", "Nova tarefa"],
    ["perfil.html", "Perfil"],
  ];
  const nav = document.createElement("nav");

  const marca = document.createElement("span");
  marca.className = "marca";
  marca.textContent = "Meu Dia";
  nav.appendChild(marca);

  for (const [link, texto] of itens) {
    const a = document.createElement("a");
    a.href = link;
    a.textContent = texto;
    if (link === atual) a.className = "atual";
    nav.appendChild(a);
  }

  const botao = document.createElement("button");
  botao.type = "button";
  botao.textContent = "Sair";
  botao.addEventListener("click", sair);
  nav.appendChild(botao);

  document.getElementById("topo").appendChild(nav);
}