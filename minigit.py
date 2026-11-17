from collections import deque

class MiniGit:
    __slots__ = (
        "__dicionario_pais",
        "__dicionario_mensagens",
        "__dicionario_branches",
        "__branch_atual",
        "__identificador_contador",
        "__passos_ultima_operacao",
    )

    def __init__(self):
        self.__dicionario_pais = {}
        self.__dicionario_mensagens = {}
        self.__dicionario_branches = {}
        self.__branch_atual = "main"
        self.__identificador_contador = 0
        self.__passos_ultima_operacao = 0
        self.__dicionario_branches["main"] = None

    @property
    def passos(self):
        return self.__passos_ultima_operacao

    @property
    def branch_atual(self):
        return self.__branch_atual

    def commitar(self, mensagem):
        if not mensagem:
            raise ValueError("A mensagem do commit não pode estar vazia.")
        
        self.__identificador_contador += 1
        identificador_commit = f"c{self.__identificador_contador}"
        
        commit_pai = self.__dicionario_branches[self.__branch_atual]
        
        if commit_pai is None:
            self.__dicionario_pais[identificador_commit] = []
        
        if commit_pai is not None:
            self.__dicionario_pais[identificador_commit] = [commit_pai]
            
        self.__dicionario_mensagens[identificador_commit] = mensagem
        self.__dicionario_branches[self.__branch_atual] = identificador_commit
        
        self.__passos_ultima_operacao = 2
        return identificador_commit

    def mensagem(self, commit):
        if commit not in self.__dicionario_mensagens:
            raise ValueError("O commit informado não existe.")
        
        self.__passos_ultima_operacao = 1
        return self.__dicionario_mensagens[commit]

    def pais(self, commit):
        if commit not in self.__dicionario_pais:
            raise ValueError("O commit informado não existe.")
        
        self.__passos_ultima_operacao = 1
        return tuple(self.__dicionario_pais[commit])

    def criar_branch(self, nome):
        if nome in self.__dicionario_branches:
            raise ValueError("A branch informada já existe.")
        
        commit_atual = self.__dicionario_branches[self.__branch_atual]
        if commit_atual is None:
            raise ValueError("Não há commits na branch atual para criar uma nova branch.")
        
        self.__dicionario_branches[nome] = commit_atual
        self.__passos_ultima_operacao = 1

    def trocar_branch(self, nome):
        if nome not in self.__dicionario_branches:
            raise ValueError("A branch informada não existe.")
        
        self.__branch_atual = nome
        self.__passos_ultima_operacao = 1

    def mesclar(self, nome):
        if nome not in self.__dicionario_branches:
            raise ValueError("A branch a ser mesclada não existe.")
        
        if nome == self.__branch_atual:
            raise ValueError("Não é possível mesclar a branch com ela mesma.")
        
        commit_atual = self.__dicionario_branches[self.__branch_atual]
        commit_alvo = self.__dicionario_branches[nome]
        
        if commit_atual is None or commit_alvo is None:
            raise ValueError("Ambas as branches precisam ter commits para realizar o merge.")
        
        self.__identificador_contador += 1
        identificador_commit = f"c{self.__identificador_contador}"
        
        self.__dicionario_pais[identificador_commit] = [commit_atual, commit_alvo]
        self.__dicionario_mensagens[identificador_commit] = f"merge de {nome}"
        self.__dicionario_branches[self.__branch_atual] = identificador_commit
        
        self.__passos_ultima_operacao = 2
        return identificador_commit

    def log(self):
        commit_inicial = self.__dicionario_branches[self.__branch_atual]
        if commit_inicial is None:
            self.__passos_ultima_operacao = 0
            return ()
        
        fila_commits = deque([commit_inicial])
        visitados = set()
        ordem_log = []
        passos_contados = 0
        
        while fila_commits:
            commit_atual = fila_commits.popleft()
            passos_contados += 1
            
            if commit_atual not in visitados:
                visitados.add(commit_atual)
                ordem_log.append(commit_atual)
                for pai in self.__dicionario_pais.get(commit_atual, []):
                    fila_commits.append(pai)
                    
        self.__passos_ultima_operacao = passos_contados
        return tuple(ordem_log)

    def buscar(self, texto):
        passos_contados = 0
        encontrado = None
        
        for i in range(1, self.__identificador_contador + 1):
            identificador_commit = f"c{i}"
            passos_contados += 1
            if texto in self.__dicionario_mensagens.get(identificador_commit, ""):
                encontrado = identificador_commit
                break
                
        self.__passos_ultima_operacao = passos_contados
        return encontrado

    def merges(self):
        passos_contados = 0
        lista_merges = []
        
        for i in range(1, self.__identificador_contador + 1):
            identificador_commit = f"c{i}"
            passos_contados += 1
            if len(self.__dicionario_pais.get(identificador_commit, [])) > 1:
                lista_merges.append(identificador_commit)
                
        self.__passos_ultima_operacao = passos_contados
        return tuple(lista_merges)


def tentar(acao):
    try:
        acao()
    except ValueError as erro:
        print("erro:", erro)


git = MiniGit()
git.commitar("primeiro commit")
print(git.passos)
git.commitar("segundo commit")
git.criar_branch("feature")
print(git.passos)
git.commitar("terceiro commit")
git.trocar_branch("feature")
git.commitar("quarto commit")
git.trocar_branch("main")
git.mesclar("feature")
print(git.pais("c5"))
print(git.log(), git.passos)
print(git.mensagem("c3"), git.passos)
print(git.buscar("quarto"), git.passos)
print(git.merges())
git.trocar_branch("feature")
print(git.log(), git.passos)
git.trocar_branch("main")

tentar(lambda: git.trocar_branch("inexistente"))
tentar(lambda: git.criar_branch("main"))
tentar(lambda: git.mesclar("main"))
tentar(lambda: git.pais("c99"))


def medir(quantidade):
    repositorio_medicao = MiniGit()
    for i in range(quantidade):
        repositorio_medicao.commitar(f"commit {i}")
    passos_commitar = repositorio_medicao.passos
    repositorio_medicao.log()
    passos_log = repositorio_medicao.passos
    return passos_commitar, passos_log


print("\n--- Tabela de Medição ---")
print("commits   passos do commitar   passos do log")
for qtd in [10, 100, 1000]:
    p_com, p_log = medir(qtd)
    print(f"{qtd:<9} {p_com:<20} {p_log}")