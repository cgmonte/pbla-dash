import requests

def get_names(tag_turma: str, **kwargs):
	tag_equipe = kwargs.get('tag_equipe')

	if tag_equipe:
		url = "http://172.22.0.8:8000/api/core/turmas/names/"
		
		# print(f'{url}{tag_turma}/{tag_equipe}/?format=json')

		response = requests.get(f'{url}{tag_turma}/{tag_equipe}/?format=json')
		response = response.json()
		
		return response
	
	else:
		url = "http://172.22.0.8:8000/api/core/turmas/names/"
		response = requests.get(f'{url}{tag_turma}/?format=json')
		response = response.json()
		
		return response
	
