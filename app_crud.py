import streamlit as st
from supabase import create_client, Client
import os

# Configurações do Supabase
SUPABASE_URL = "https://mwvjsdxbnraqjamjdtqy.supabase.co"  # Substitua pelo seu URL do Supabase
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im13dmpzZHhibnJhcWphbWpkdHF5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDk3MzM3MjYsImV4cCI6MjA2NTMwOTcyNn0.y2JkLAWU3u6bwTvY8jbjQSH0cnohwffkC7ER5YHMaFg"  # Substitua pela sua chave de API do Supabase

# Inicializa o cliente do Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Funções para operações no banco de dados
def add_product(nome, marca, descricao, dt_compra, dt_val, quantidade, valor):
    try:
        supabase.table("produtos").insert({
            "nome": nome,
            "marca": marca,
            "descricao": descricao,
            "dt_compra": dt_compra.isoformat(),
            "dt_val": dt_val.isoformat(),
            "quantidade": quantidade,
            "valor": valor
        }).execute()
        st.success("Produto adicionado com sucesso!")
    except Exception as e:
        st.error(f"Erro ao adicionar produto: {e}")

def update_product(id, nome, marca, descricao, dt_compra, dt_val, quantidade, valor):
    try:
        supabase.table("produtos").update({
            "nome": nome,
            "marca": marca,
            "descricao": descricao,
            "dt_compra": dt_compra.isoformat(),
            "dt_val": dt_val.isoformat(),
            "quantidade": quantidade,
            "valor": valor
        }).eq("id", id).execute()
        st.success("Produto atualizado com sucesso!")
    except Exception as e:
        st.error(f"Erro ao atualizar produto: {e}")

def view_products():
    try:
        result = supabase.table("produtos").select("*").execute()
        if result.data:
            for row in result.data:
                st.write(f"| ID: {row['id']} | Nome: {row['nome']} | Marca: {row['marca']} | Descrição: {row['descricao']} | Data da compra: {row['dt_compra']} | Data de validade: {row['dt_val']} | Quantidade: {row['quantidade']} | Valor: {row['valor']} |")
                st.divider()
        else:
            st.info("Nenhum registro encontrado.")
    except Exception as e:
        st.error(f"Erro ao buscar produtos: {e}")

def delete_product(id):
    try:
        supabase.table("produtos").delete().eq("id", id).execute()
        st.success("Produto excluído com sucesso!")
    except Exception as e:
        st.error(f"Erro ao excluir produto: {e}")

def search_products(field, value):
    try:
        result = supabase.table("produtos").select("*").eq(field, value).execute()
        if result.data:
            for row in result.data:
                st.write(f"| ID: {row['id']} | Nome: {row['nome']} | Marca: {row['marca']} | Descrição: {row['descricao']} | Data da compra: {row['dt_compra']} | Data de validade: {row['dt_val']} | Quantidade: {row['quantidade']} | Valor: {row['valor']} |")
        else:
            st.write("Nenhum resultado encontrado")
    except Exception as e:
        st.error(f"Erro ao buscar produtos: {e}")

def total_products():
    try:
        result = supabase.table("produtos").select("*").execute()
        quantidade_total = sum(row['quantidade'] for row in result.data)
        st.subheader(f"Total de produtos no estoque: {quantidade_total}")
    except Exception as e:
        st.error(f"Erro ao calcular total de produtos: {e}")

def total_value():
    try:
        result = supabase.table("produtos").select("*").execute()
        valor_total = sum(row['valor'] * row['quantidade'] for row in result.data)
        st.subheader(f"Total de valor no estoque: {valor_total}")
    except Exception as e:
        st.error(f"Erro ao calcular total de valor: {e}")

# Função principal da aplicação
def main():
    st.title("Sistema de Estoque")
    option = st.sidebar.selectbox("Selecione uma opção", ("Adicione", "Veja", "Atualize", "Exclua", "Pesquisar", "Total de produto", "Total de valor"))

    if option == "Adicione":
        st.subheader("Adicione um produto")
        nome = st.text_input("Entre com o nome")
        marca = st.text_input("Entre com a marca")
        descricao = st.text_input("Entre com a descrição")
        dt_compra = st.date_input("Entre com a data da compra")
        dt_val = st.date_input("Entre com a data de validade")
        quantidade = st.number_input("Entre com a quantidade", min_value=0)
        valor = st.number_input("Entre com o valor", min_value=0.0)

        if st.button("Adicione"):
            if nome and marca and descricao and dt_compra and dt_val and quantidade and valor:
                add_product(nome, marca, descricao, dt_compra, dt_val, quantidade, valor)
            else:
                st.error("Preencha todos os campos!")

    elif option == "Veja":
        st.subheader("Veja o estoque")
        view_products()

    elif option == "Atualize":
        st.subheader("Atualize produtos")
        id = st.number_input("Digite o ID do produto", min_value=1)
        try:
            result = supabase.table("produtos").select("*").eq("id", id).execute()
            if not result.data:
                st.error("Produto não encontrado!")
            else:
                row = result.data[0]
                nome = st.text_input("Entre com o nome", value=row['nome'])
                marca = st.text_input("Entre com a marca", value=row['marca'])
                descricao = st.text_input("Entre com a descrição", value=row['descricao'])
                dt_compra = st.date_input("Entre com a data da compra", value=row['dt_compra'])
                dt_val = st.date_input("Entre com a data de validade", value=row['dt_val'])
                quantidade = st.number_input("Entre com a quantidade", value=row['quantidade'])
                valor = st.number_input("Entre com o valor", value=row['valor'])
                if st.button("Atualizar"):
                    update_product(id, nome, marca, descricao, dt_compra, dt_val, quantidade, valor)
        except Exception as e:
            st.error(f"Erro ao atualizar produto: {e}")

    elif option == "Exclua":
        st.subheader("Exclua um produto")
        id = st.number_input("Digite o ID do produto", min_value=1)
        if st.button("Excluir"):
            delete_product(id)

    elif option == "Pesquisar":
        st.subheader("Pesquise produtos")
        choice = st.selectbox("Escolha o campo que deseja pesquisar", ["Nome", "Marca", "Descrição", "Data de compra", "Data de validade", "Quantidade", "Valor"])
        if choice == "Nome":
            pesquisa = st.text_input("Digite o nome a ser pesquisado")
            if pesquisa:
                search_products("nome", pesquisa)
        elif choice == "Marca":
            pesquisa = st.text_input("Digite a marca a ser pesquisada")
            if pesquisa:
                search_products("marca", pesquisa)
        elif choice == "Descrição":
            pesquisa = st.text_input("Digite a descricao a ser pesquisada")
            if pesquisa:
                search_products("descricao", pesquisa)
        elif choice == "Data de compra":
            pesquisa = st.date_input("Coloque a data a ser pesquisada")
            if pesquisa:
                search_products("dt_compra", pesquisa.isoformat())
        elif choice == "Data de validade":
            pesquisa1 = st.date_input("Insira a primeira data do periodo")
            pesquisa2 = st.date_input("Insira a segunda data do periodo")
            if pesquisa1 and pesquisa2:
                try:
                    result = supabase.table("produtos").select("*").gte("dt_val", pesquisa1.isoformat()).lte("dt_val", pesquisa2.isoformat()).execute()
                    if result.data:
                        for row in result.data:
                            st.write(f"| ID: {row['id']} | Nome: {row['nome']} | Marca: {row['marca']} | Descrição: {row['descricao']} | Data da compra: {row['dt_compra']} | Data de validade: {row['dt_val']} | Quantidade: {row['quantidade']} | Valor: {row['valor']} |")
                    else:
                        st.write("Nenhum resultado encontrado")
                except Exception as e:
                    st.error(f"Erro ao buscar produtos: {e}")
        elif choice == "Quantidade":
            pesquisa = st.number_input("Coloque a quantidade a ser pesquisada")
            if pesquisa:
                search_products("quantidade", pesquisa)
        elif choice == "Valor":
            pesquisa = st.number_input("Coloque o valor a ser pesquisado")
            if pesquisa:
                search_products("valor", pesquisa)

    elif option == "Total de produto":
        total_products()

    elif option == "Total de valor":
        total_value()

# Executa a aplicação
if __name__ == "__main__":
    main()
