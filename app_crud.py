import streamlit as st
import psycopg2
from psycopg2 import sql
import os
from st_supabase_connection import SupabaseConnection

# Função para estabelecer conexão com o banco de dados MySQL
password = os.getenv(
"Amoracolorida1!"
)
def get_db_connection():
    try:
        con = st.connection("supabase",type=SupabaseConnection)
        return con
    except Exception as e:
        st.error(f"Erro ao conectar ao banco de dados: {e}")
        return None

# Estabelece a conexão
con = get_db_connection()
cursor = con.cursor()
if con:
    st.success("Conexão estabelecida com o banco de dados MySQL!")
else:
    st.error("Erro de conexão")

# Funções para operações no banco de dados
def add_product(nome, marca, descricao, dt_compra, dt_val, quantidade, valor):
    try:
        cursor = con.cursor()
        cursor.execute(
            "INSERT INTO produtos (nome, marca, descricao, dt_compra, dt_val, quantidade, valor) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (nome, marca, descricao, dt_compra, dt_val, quantidade, valor)
        )
        con.commit()
        st.success("Produto adicionado com sucesso!")
    except Exception as e:
        st.error(f"Erro ao adicionar produto: {e}")
    finally:
        cursor.close()

def update_product(id, nome, marca, descricao, dt_compra, dt_val, quantidade, valor):
    try:
        cursor = con.cursor()
        cursor.execute(
        """
        UPDATE produtos
        SET nome = %s, marca = %s, descricao = %s, dt_compra = %s, dt_val = %s, quantidade = %s, valor = %s
        WHERE id = %s
        """,
        (nome, marca, descricao, dt_compra, dt_val, quantidade, valor, id)
        )
        con.commit()
        st.success("Produto atualizado com sucesso!")
    except Exception as e:
        st.error(f"Erro ao atualizar produto: {e}")
    finally:
        cursor.close()
def view_products():
    try:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM produtos")
        result = cursor.fetchall()
        if result:
            for row in result:
                st.write(f"| ID: {row[0]} | Nome: {row[1]} | Marca: {row[2]} | Descrição: {row[3]} | Data da compra: {row[4]} | Data de validade: {row[5]} | Quantidade: {row[6]} | Valor: {row[7]} |")
                st.divider()
        else:
            st.info("Nenhum registro encontrado.")
    except Exception as e:
        st.error(f"Erro ao buscar produtos: {e}")
    finally:
        cursor.close()

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
            cursor.execute("SELECT nome, marca, descricao, dt_compra, dt_val, quantidade, valor FROM produtos WHERE id = %s", (id,))
            result = cursor.fetchone()

            # Verifica se o produto existe no banco
            if not result:
                st.error("Produto não encontrado!")
            else:
                # Exibe os valores para edição
                nome = st.text_input("Entre com o nome", value=result[0])
                marca = st.text_input("Entre com a marca", value=result[1])
                descricao = st.text_input("Entre com a descrição", value=result[2])
                dt_compra = st.date_input("Entre com a data da compra", value=result[3])
                dt_val = st.date_input("Entre com a data de validade", value=result[4])
                quantidade = st.number_input("Entre com a quantidade", value=int(result[5]))
                valor = st.number_input("Entre com o valor", value=float(result[6]))
                if st.button("Atualizar"):
                    try:
                        update_product(id, nome, marca, descricao, dt_compra, dt_val, quantidade, valor)
                    except Exception as e:
                        st.error(f"Erro ao atualizar produto: {e}")
        except Exception as e:
            st.error(f"Erro ao atualizar produto: {e}")     


    elif option == "Exclua":
        st.subheader("Exclua um produto")
        id = st.number_input("Digite o ID do produto", min_value=1)
        if st.button("Excluir"):
            try:
                cursor.execute("DELETE FROM produtos WHERE id = %s", (id,))
                con.commit()
                st.success("Produto excluído com sucesso!")
            except Exception as e:
                st.error(f"Error: {e}")

    elif option == "Pesquisar":
        st.subheader("Pesquise produtos")
        choice = st.selectbox("Escolha o campo que deseja pesquisar", ["Nome", "Marca", "Descrição", "Data de compra", "Data de validade", "Quantidade", "Valor"])
        #NOME
        if choice == "Nome":
            pesquisa = st.text_input("Digite o nome a ser pesquisado")
            try:
                cursor.execute("SELECT id, nome, marca, descricao, dt_compra, dt_val, quantidade, valor FROM produtos WHERE nome LIKE %s;", (f"%{pesquisa}%",))
                result = cursor.fetchall()
                if result:
                    for row in result:
                        st.write(f"| ID: {row[0]} | Nome: {row[1]} | Marca: {row[2]} | Descrição: {row[3]} | Data da compra: {row[4]} | Data de validade: {row[5]} | Quantidade: {row[6]} | Valor: {row[7]} |")
                else:
                    st.write("Nenhum resultado encontrado")
            except Exception as e:
                st.error(f"Error: {e}")
        #MARCA
        elif choice == "Marca":
            pesquisa = st.text_input("Digite a marca a ser pesquisada")
            try:
                cursor.execute("SELECT id, nome, marca, descricao, dt_compra, dt_val, quantidade, valor FROM produtos WHERE marca LIKE %s;", (f"%{pesquisa}%",))
                result = cursor.fetchall()
                if result:
                    for row in result:
                        st.write(f"| ID: {row[0]} | Nome: {row[1]} | Marca: {row[2]} | Descrição: {row[3]} | Data da compra: {row[4]} | Data de validade: {row[5]} | Quantidade: {row[6]} | Valor: {row[7]} |")
                else:
                    st.write("Nenhum resultado encontrado")
            except Exception as e:
                st.error(f"Error: {e}")
        #DESCRICAO
        elif choice == "Descrição":
            pesquisa = st.text_input("Digite a descricao a ser pesquisada")
            try:
                cursor.execute("SELECT id, nome, marca, descricao, dt_compra, dt_val, quantidade, valor FROM produtos WHERE descricao LIKE %s;", (f"%{pesquisa}%",))
                result = cursor.fetchall()
                if result:
                    for row in result:
                        st.write(f"| ID: {row[0]} | Nome: {row[1]} | Marca: {row[2]} | Descrição: {row[3]} | Data da compra: {row[4]} | Data de validade: {row[5]} | Quantidade: {row[6]} | Valor: {row[7]} |")
                else:
                        st.write("Nenhum resultado encontrado")
            except Exception as e:
                    st.error(f"Error: {e}")
        #DATA DE COMPRA
        elif choice == "Data de compra":
            pesquisa = st.date_input("Coloque a data a ser pesquisada")
            try:
                cursor.execute("SELECT id, nome, marca, descricao, dt_compra, dt_val, quantidade, valor FROM produtos WHERE dt_compra = %s;", (pesquisa,))
                result = cursor.fetchall()
                if result:
                    for row in result:
                        st.write(f"| ID: {row[0]} | Nome: {row[1]} | Marca: {row[2]} | Descrição: {row[3]} | Data da compra: {row[4]} | Data de validade: {row[5]} | Quantidade: {row[6]} | Valor: {row[7]} |")
                else:
                    st.write("Nenhum resultado encontrado")
            except Exception as e:
                        st.error(f"Error: {e}")
        #DATA DE VALIDADE
        elif choice == "Data de validade":
            pesquisa1 = st.date_input("Insira a primeira data do periodo")
            pesquisa2 = st.date_input("Insira a segunda data do periodo")
            try:
                cursor.execute("SELECT id, nome, marca, descricao, dt_compra, dt_val, quantidade, valor FROM produtos WHERE dt_val BETWEEN %s AND %s;", (pesquisa1, pesquisa2,))
                result = cursor.fetchall()
                if result:
                    for row in result:
                        st.write(f"| ID: {row[0]} | Nome: {row[1]} | Marca: {row[2]} | Descrição: {row[3]} | Data da compra: {row[4]} | Data de validade: {row[5]} | Quantidade: {row[6]} | Valor: {row[7]} |")
                else:
                    st.write("Nenhum resultado encontrado")
            except Exception as e:
                        st.error(f"Error: {e}")
        #QUANTIDADE
        elif choice == "Quantidade":
            pesquisa = st.number_input("Coloque a quantidade a ser pesquisada")
            try:
                cursor.execute("SELECT id, nome, marca, descricao, dt_compra, dt_val, quantidade, valor FROM produtos WHERE quantidade = %s;", (pesquisa,))
                result = cursor.fetchall()
                if result:
                    for row in result:
                        st.write(f"| ID: {row[0]} | Nome: {row[1]} | Marca: {row[2]} | Descrição: {row[3]} | Data da compra: {row[4]} | Data de validade: {row[5]} | Quantidade: {row[6]} | Valor: {row[7]} |")
                else:
                    st.write("Nenhum resultado encontrado")
            except Exception as e:
                        st.error(f"Error: {e}")
        #VALOR
        elif choice == "Valor":
            pesquisa = st.number_input("Coloque o valor a ser pesquisado")
            try:
                cursor.execute("SELECT id, nome, marca, descricao, dt_compra, dt_val, quantidade, valor FROM produtos WHERE valor = %s;", (pesquisa,))
                result = cursor.fetchall()
                if result:
                    for row in result:
                        st.write(f"| ID: {row[0]} | Nome: {row[1]} | Marca: {row[2]} | Descrição: {row[3]} | Data da compra: {row[4]} | Data de validade: {row[5]} | Quantidade: {row[6]} | Valor: {row[7]} |")
                else:
                    st.write("Nenhum resultado encontrado")
            except Exception as e:
                        st.error(f"Error: {e}")


    #Total de produto
    elif option == "Total de produto":
        cursor.execute("SELECT * FROM produtos;")
        result = cursor.fetchall()
        quantidade_total = 0
        for row in result:
            quantidade_total = quantidade_total + row[6]
        st.subheader(f"Total de produtos no estoque: {quantidade_total}")

    #Total de valor
    elif option == "Total de valor":
        cursor.execute("SELECT * FROM produtos;")
        result = cursor.fetchall()
        valor_total = 0
        for row in result:
            valor_total = valor_total + (row[7] * row[6])
        st.subheader(f"Total de produtos no estoque: {valor_total}")

# Executa a aplicação
if __name__ == "__main__":
    main()
