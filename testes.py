import unittest
import json
from app import criar_app
from banco_dados import db

class TesteNarrado(unittest.TestCase):
    def setUp(self):
        
        self.app = criar_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
        
        print("\n---------------------------------------------------")
        print("🤖 INICIANDO AMBIENTE DE TESTE (Banco em Memória)")

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
        print("🏁 FIM DO TESTE - Limpeza concluída.")
        print("---------------------------------------------------")

    def test_ciclo_completo_da_api(self):
        """Executa todos os passos e narra o resultado."""
        
        # 1. VERIFICAR API ONLINE
        print("\n[1] Verificando se a API está online...")
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        print("   ✅ SUCESSO: A API respondeu 200 OK.")

        # 2. REGISTRAR USUÁRIO
        print("\n[2] Tentando registrar usuário 'mariadias'...")
        res_registro = self.client.post('/api/usuarios/registrar', json={
            'nome_usuario': 'mariadias', 'email': 'maria@teste.com', 'senha': '123'
        })
        self.assertEqual(res_registro.status_code, 201)
        print("   ✅ SUCESSO: Usuário criado.")

        # 3. FAZER LOGIN
        print("\n[3] Tentando fazer login para pegar o Token...")
        res_login = self.client.post('/api/usuarios/login', json={
            'nome_usuario': 'mariadias', 'senha': '123'
        })
        self.assertEqual(res_login.status_code, 200)
        token = res_login.json['token']
        headers = {'Authorization': f'Bearer {token}'}
        print("   ✅ SUCESSO: Login feito. Token recebido.")

        # 4. CRIAR LIVRO
        print("\n[4] Criando o livro 'Dom Quixote'...")
        livro_data = {
            'titulo': 'Dom Quixote',
            'autor': 'Miguel de Cervantes',
            'data_publicacao': '1605',
            'isbn': '123-456'
        }
        res_criar = self.client.post('/api/livros', headers=headers, json=livro_data)
        self.assertEqual(res_criar.status_code, 201)
        id_livro = res_criar.json['livro']['id']
        print(f"   ✅ SUCESSO: Livro criado com ID {id_livro}.")

        # 5. LISTAR LIVROS
        print("\n[5] Listando livros para conferir...")
        res_lista = self.client.get('/api/livros', headers=headers)
        self.assertEqual(len(res_lista.json), 1)
        self.assertEqual(res_lista.json[0]['titulo'], 'Dom Quixote')
        print("   ✅ SUCESSO: A lista retornou exatamente 1 livro correto.")

        # 6. ATUALIZAR LIVRO
        print("\n[6] Atualizando título para 'Dom Quixote - Edição Especial'...")
        res_update = self.client.put(f'/api/livros/{id_livro}', headers=headers, json={
            'titulo': 'Dom Quixote - Edição Especial'
        })
        self.assertEqual(res_update.status_code, 200)
        print("   ✅ SUCESSO: Livro atualizado.")

        # 7. DELETAR LIVRO
        print("\n[7] Deletando o livro...")
        res_delete = self.client.delete(f'/api/livros/{id_livro}', headers=headers)
        self.assertEqual(res_delete.status_code, 200)
        
        # Confirmação final de que está vazio
        res_confirma = self.client.get('/api/livros', headers=headers)
        self.assertEqual(len(res_confirma.json), 0)
        print("   ✅ SUCESSO: Livro deletado e lista está vazia.")

if __name__ == '__main__':
    # verbosity=0 remove o padrão do unittest para focar nos nossos prints
    unittest.main(verbosity=0)