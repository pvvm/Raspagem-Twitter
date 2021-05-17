# Importando as bibliotecas necessárias
import snscrape.modules.twitter as sntwitter
import tkinter as tk
import io


def tweets_search(dados):
	# Recebo os dados enviados pelo usuário
	username = dados[0]
	start_date = dados[1].split('-')
	end_date = dados[2].split('-')
	type_search = dados[3]
	num_search = dados[4]
	keywords = dados[5].split(',')

	# Evita que usuários deixem de preencher algo
	#if keywords == [''] or start_date == [''] or end_date == ['']:
	#	return render(dados, 'portal/tweets_search.html')

	# Adapto a data no formato DD-MM-AAAA para AAAA-MM-DD
	begin_date = f'{start_date[2]}-{start_date[1]}-{start_date[0]}'
	end_date = f'{end_date[2]}-{end_date[1]}-{end_date[0]}'

	num = len(keywords)
	j = 0
	# Crio a string que determina a raspagem a ser feita
	search = ''
	while num > j:
		# Caso tenha usuário, defino que deve ser concatenado seu username
		if username != '' and j == 0:
			search = search + f'from:{username}'
		# Concateno a primeira keyword
		if j == 0:
			search = search + f' {keywords[0]}'
		# Concateno as demais keywords
		else:
		# Concateno com AND caso deseje tweets com todos as keywords
			if type_search == 'all-kw':
				search = search + f' AND {keywords[j]}'
		# Concateno com OR caso deseje tweets com no mínimo uma keyword
			else:
				search = search + f' OR {keywords[j]}'
		j += 1

	# Concateno as datas de início e fim da busca
	search = search+ f' since:{begin_date}' + f' until:{end_date}'

	tweets = []
	# Realiza a busca definida anteriormente, se limitando com o número máximo de tweets
	with io.open('tweets.txt', 'w', encoding='utf-8') as f:
		for i, tweet in enumerate(sntwitter.TwitterSearchScraper(search).get_items()):
			if num_search != 'Ilimitado' and i > int(num_search):
				break
			
			# Recebe e formata a data do tweet
			data = str(tweet.date).split()[0]
			data = data.split('-')
			data = f'{data[2]}-{data[1]}-{data[0]}'
			tweets.append([data, tweet.content])

			f.write(data)
			f.write('\n')
			f.write(tweet.content)
			f.write('\n\n')

def raspar():
	dados = []
	dados.append(usuario.get())
	dados.append(data_inicio.get())
	dados.append(data_fim.get())
	if variavel1.get() == 'todas as palavras-chave':
		dados.append('all-kw')
	else:
		dados.append('min-one')
	dados.append(variavel2.get())
	dados.append(palavras.get())
	tweets_search(dados)


window = tk.Tk()
window.title('Raspagem no Twitter')

greeting = tk.Label(text="Bem-vindo ao sistema de raspagem no Twitter", width=50, heigh=3, font=30)
greeting.pack()

label = tk.Label(text="Digite o nome do usuário (Opcional)", height=3)
label.pack()

usuario = tk.Entry()
usuario.pack()

label = tk.Label(text="Digite a data de início da busca (DD-MM-AAAA)", height=3)
label.pack()

data_inicio = tk.Entry()
data_inicio.pack()


label = tk.Label(text="Digite a data de fim da busca (DD-MM-AAAA)", height=3)
label.pack()

data_fim = tk.Entry()
data_fim.pack()

label = tk.Label(text="O tweet deve conter:", height=3)
label.pack()

variavel1 = tk.StringVar(window)
variavel1.set("todas as palavras-chave")
tipo = tk.OptionMenu(window, variavel1, "todas as palavras-chave", "no mínimo uma palavra-chave")
tipo.pack()

label = tk.Label(text="Número de tweets retornados:", height=3)
label.pack()

variavel2 = tk.StringVar(window)
variavel2.set("Ilimitado")
num = tk.OptionMenu(window, variavel2, "Ilimitado", "200", "100", "50")
num.pack()

label = tk.Label(text="Digite as palavras-chave (separadas por vírgula)", height=3)
label.pack()

palavras = tk.Entry()
palavras.pack()

button = tk.Button(master=window, text='Raspar', command=raspar, height=2, width=7)
button.pack(pady=10)

window.mainloop()