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

def get_integrantes(tag_equipe: int):
	url = 'http://172.22.0.8:8000/api/core/equipe/'
	response = requests.get(f'{url}{tag_equipe}/users/?format=json')
	response = response.json()
	return response

def update_gdrive_records(pbla_uid: int):
	url = f"http://pbla_gdrive_1/api/integ/gdrive/user/update/records?user_id={pbla_uid}"
	response = requests.post(url)
	# print(response)
	return response.status_code

