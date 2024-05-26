from bottle import Bottle, run, request, template

app = Bottle()

# Simulação de uma base de dados de cartões de visita
business_cards = [
    {"name": "John Doe", "title": "Software Engineer", "pagina_online": "http://johndoe.com", "instagram": "@john_doe", "classification": "Educação", "phone": "123-456-7890"},
    {"name": "Jane Smith", "title": "Data Scientist", "pagina_online": "http://janesmith.com", "instagram": "@jane_smith", "classification": "Permacultura", "phone": "987-654-3210"},
]

# Classe para gerenciar o resumo das atividades (Abstract)
class PersonAbstract:
    def __init__(self, name, abstract):
        self.name = name
        self.abstract = abstract

# Simulação de uma base de dados para abstracts
person_abstracts = [
    PersonAbstract("John Doe", "Experienced software engineer with a passion for developing innovative programs."),
    PersonAbstract("Jane Smith", "Data scientist who loves uncovering insights from complex datasets."),
]

# Página inicial para visualizar e adicionar cartões de visita
@app.route('/')
def index():
    classification = request.query.classification
    name = request.query.name
    if classification:
        filtered_cards = [card for card in business_cards if card["classification"] == classification]
    else:
        filtered_cards = business_cards
    
    selected_card = next((card for card in business_cards if card["name"] == name), None) if name else None
    selected_abstract = next((abstract for abstract in person_abstracts if abstract.name == name), None) if name else None

    return template('''
        <h2>Cartões de Visita</h2>
        <form action="/" method="get">
            <select name="classification">
                <option value="">Todas</option>
                <option value="Artes">Artes</option>
                <option value="Bioconstrução">Bioconstrução</option>
                <option value="Educação">Educação</option>
                <option value="Permacultura">Permacultura</option>
            </select>
            <input type="submit" value="Filtrar">
        </form>
        <ul>
            % for card in filtered_cards:
                <li>
                    {{card["name"]}} - {{card["title"]}} - 
                    <a href="{{card["pagina_online"]}}" target="_blank">Página Online</a> - 
                    <a href="https://instagram.com/{{card["instagram"]}}" target="_blank">Instagram</a> - 
                    {{card["classification"]}}
                </li>
            % end
        </ul>
        
        <h2>Adicionar Novo Cartão de Visita</h2>
        <form action="/add" method="post">
            Nome: <input type="text" name="name"><br>
            Título: <input type="text" name="title"><br>
            Página Online: <input type="text" name="pagina_online"><br>
            Instagram: <input type="text" name="instagram"><br>
            Telefone: <input type="text" name="phone"><br>
            Classificação:
            <select name="classification">
                <option value="Artes">Artes</option>
                <option value="Bioconstrução">Bioconstrução</option>
                <option value="Educação">Educação</option>
                <option value="Permacultura">Permacultura</option>
            </select><br>
            <input type="submit" value="Adicionar">
        </form>

        <h2>Buscar Resumo por Nome</h2>
        <form action="/" method="get">
            <select name="name">
                <option value="">Selecione um nome</option>
                % for card in business_cards:
                    <option value="{{card["name"]}}">{{card["name"]}}</option>
                % end
            </select>
            <input type="submit" value="Buscar">
        </form>

        % if selected_card:
            <h2>Resumo das Atividades</h2>
            <p>Nome: {{selected_card["name"]}}</p>
            <p>Título: {{selected_card["title"]}}</p>
            <p>Página Online: <a href="{{selected_card["pagina_online"]}}" target="_blank">{{selected_card["pagina_online"]}}</a></p>
            <p>Instagram: <a href="https://instagram.com/{{selected_card["instagram"]}}" target="_blank">{{selected_card["instagram"]}}</a></p>
            <p>Classificação: {{selected_card["classification"]}}</p>
            % if selected_abstract:
                <p>Abstract: {{selected_abstract.abstract}}</p>
            % else:
                <form action="/add_abstract" method="post">
                    <input type="hidden" name="name" value="{{selected_card["name"]}}">
                    Abstract: <textarea name="abstract"></textarea><br>
                    <input type="submit" value="Adicionar Abstract">
                </form>
            % end
        % end
    ''', filtered_cards=filtered_cards, business_cards=business_cards, selected_card=selected_card, selected_abstract=selected_abstract)

# Rota para lidar com a adição de novos cartões de visita
@app.route('/add', method='POST')
def add_card():
    name = request.forms.get('name')
    title = request.forms.get('title')
    pagina_online = request.forms.get('pagina_online')
    instagram = request.forms.get('instagram')
    phone = request.forms.get('phone')
    classification = request.forms.get('classification')
    business_cards.append({"name": name, "title": title, "pagina_online": pagina_online, "instagram": instagram, "classification": classification, "phone": phone})
    return template('''
        <p>Cartão de visita adicionado com sucesso!</p>
        <a href="/">Voltar para a página inicial</a>
    ''')

# Rota para lidar com a adição de abstracts
@app.route('/add_abstract', method='POST')
def add_abstract():
    name = request.forms.get('name')
    abstract = request.forms.get('abstract')
    person_abstracts.append(PersonAbstract(name, abstract))
    return template('''
        <p>Abstract adicionado com sucesso!</p>
        <a href="/">Voltar para a página inicial</a>
    ''')

# Rota para deletar um cartão de visita e seu abstract
@app.route('/delete', method='POST')
def delete_card():
    name = request.forms.get('name')
    global business_cards
    global person_abstracts
    business_cards = [card for card in business_cards if card["name"] != name]
    person_abstracts = [abstract for abstract in person_abstracts if abstract.name != name]
    return template('''
        <p>Cartão de visita deletado com sucesso!</p>
        <a href="/dados">Voltar para a página de dados</a>
    ''')

# Rota secreta para visualizar toda a base de dados
@app.route('/dados')
def dados():
    return template('''
        <h2>Base de Dados de Cartões de Visita</h2>
        <ul>
            % for card in business_cards:
                <li>
                    Nome: {{card["name"]}}<br>
                    Título: {{card["title"]}}<br>
                    Página Online: {{card["pagina_online"]}}<br>
                    Instagram: {{card["instagram"]}}<br>
                    Telefone: {{card["phone"]}}<br>
                    Classificação: {{card["classification"]}}<br>
                    <form action="/delete" method="post" style="display:inline;">
                        <input type="hidden" name="name" value="{{card["name"]}}">
                        <input type="submit" value="Deletar">
                    </form>
                </li>
            % end
        </ul>
        <h2>Base de Dados de Abstracts</h2>
        <ul>
            % for abstract in person_abstracts:
                <li>
                    Nome: {{abstract.name}}<br>
                    Abstract: {{abstract.abstract}}<br>
                </li>
            % end
        </ul>
        <a href="/">Voltar para a página inicial</a>
    ''', business_cards=business_cards, person_abstracts=person_abstracts)

# Executar o servidor Bottle
if __name__ == '__main__':
    run(app, host='localhost', port=8080)
