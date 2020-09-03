# -*- encoding: utf-8 -*-

# @CSFelix
# Jogo da Forca

# Importações
from random import choice

# Função de leitura do arquivo
def ler_txt():
	palavras = None

	with open('words.txt', 'r') as txt:
		palavras = list(txt)
		palavras = [elemento.replace('\n', '') for elemento in palavras] # retira o caractere \n do final

	return palavras

# Função para busca de índices
def encontra_index(caractere, palavra):
	for index, elemento in list(enumerate(palavra)):
		if elemento == caractere: yield index # se o caractere buscado for encontrado, função retorna
		# o índice dele num iterator

# Classe Forca
class Forca():

	# Título do Jogo
	titulo = ('*' * len('* Jogo da Forca *') \
		+ '\n* Jogo da Forca *\n' \
		+ '*' * len('* Jogo da Forca *') \
		+ '\n')

	# Desenho do Enforcado
	desenho = [
		' *-----*\n' + \
		' |     |\n' + \
		'       |\n' + \
		'       |\n' + \
		'       |\n' + \
		'    =======\n'
		,

		' *-----*\n' + \
		' |     |\n' + \
		' O     |\n' + \
		'       |\n' + \
		'       |\n' + \
		'    =======\n'
		,
		
		' *-----*\n' + \
		' |     |\n' + \
		' O     |\n' + \
		' |     |\n' + \
		'       |\n' + \
		'    =======\n'
		,

		' *-----*\n' + \
		' |     |\n' + \
		' O     |\n' + \
		'/|     |\n' + \
		'       |\n' + \
		'    =======\n'
		,

		' *-----*\n' + \
		' |     |\n' + \
		' O     |\n' + \
		'/|\\    |\n' + \
		'       |\n' + \
		'    =======\n'
		,

		' *-----*\n' + \
		' |     |\n' + \
		' O     |\n' + \
		'/|\\    |\n' + \
		'/      |\n' + \
		'    =======\n'
		,

		' *-----*\n' + \
		' |     |\n' + \
		' O     |\n' + \
		'/|\\    |\n' + \
		'/ \\    |\n' + \
		'    =======\n'
	]

	# Construtor
	def __init__(self, lista_palavras):

		# Atribuição de atributos #
		self.palavra = choice(lista_palavras).lower() # palavra é convertida em minúscula
		self.campos = ['_'] * len(self.palavra)
		self.letras_corretas, self.letras_erradas = [], []

		self.alerta = '' # alertas ao usuário

		self.ponto_total = len(self.palavra.replace(' ', '')) # conta os caracteres da palavra
		# desconsiderando os espaços (usuário não precisa adivinhar os espaços)
		self.ponto_atual = 0 # acertos efetuados pelo usuário >> serve de flag para verificar
		# se usuário venceu o jogo

		self.venceu = None # flag de fim de jogo >> True: vitória, False: derrota

		# Substituição do caractere '_' por ' ' quando houver espaços na palavra escolhida
		self.correcao_campo()

		# Processamento do game #
		print(self.titulo)
		self.rodada()

	# Substitui campos por espaços quando houver tal caractere na palavra
	def correcao_campo(self):

		qnt_espacos = self.palavra.count(' ') # conta quantas vezes o caractere espaço aparece na palavra
		index_inicio = 0 # index de início para substituição do campo de espaço
		index_atual = 0 # última index substituída

		# Processo de substituição
		for i in range(0, qnt_espacos):
			self.campos[self.palavra.index(' ', index_inicio)] = ' ' # index_inicio representa a posição de
			# início da string a ser considerada para consulta do caractere

			index_atual = self.palavra.index(' ', index_inicio) # encontra índice que foi alterada

			index_inicio = self.palavra.index(' ', index_atual) + 1 # é preciso somar por 1 a fim de não
			# repetir a mesma index nas substituições

	# Processamento de cada rodada do game
	def rodada(self):
		# Loop de rodadas
		while True:

			# Desenho da forca
			print(self.desenho[len(self.letras_erradas)])
			print('Letras Erradas: %s' % (self.letras_erradas))
			print('Letras Corretas: %s' % (self.letras_corretas))
			print('\nPalavra:')
			print(*self.campos) # o asterístico printa cada elemento da lista separado por espaço
			# ele não funciona com a formatação pelo operador '%'
			print(self.alerta)

			# Leitura da letra
			letra = input('Letra: ')
			print('\n')

			# Usuário digitou uma letra
			if letra.isalpha():
				letra = letra.lower()

				# Letra já digitada
				if (letra in self.letras_erradas) or (letra in self.letras_corretas): self.alerta = '\n** Letra já escolhida: %s. **' \
				% (letra)

				# Letra errada
				elif letra not in self.palavra: self.letras_erradas.append(letra)

				# Letra correta
				else:
					# Zeramento do alerta
					self.alerta = ''

					# Exibição da letra em seus respectivos campos
					indices = list(encontra_index(letra, self.palavra))
					for i in indices: self.campos[i] = letra

					# Incrementação dos acertos
					self.ponto_atual += len(indices)

					self.letras_corretas.append(letra)

			# Usuário não digitou uma letra
			else: self.alerta = '\n** Apenas letras são válidas: %s. **' % (letra)

			# Fim de jogo
			if (self.ponto_atual == self.ponto_total) or (len(self.letras_erradas) == 6):
				
				# Vitória
				if self.ponto_atual == self.ponto_total: 
					self.venceu = True
					break
				
				# Derrota
				else: 
					self.venceu = False
					break

		# Chamada do Game Over
		self.game_over()

	# Mensagem de Game Over
	def game_over(self):
		
		# Vitória
		if self.venceu:
			
			# Palavra correta com caracteres separados por espaço
			palavra = ''
			for letra in self.campos: palavra += letra + ' '

			# Alerta
			self.alerta = '*' * len('** Parabéns, você venceu!! **') + \
			'\n** Parabéns, você venceu!! **\n' + \
			'*' * len('** Parabéns, você venceu!! **') + \
			'\n%s' % (palavra)

		# Derrota
		else:
			self.alerta = self.desenho[6] + '\n' + \
			'*' * len('** Que pena, você perdeu :( **') + \
			'\n** Que pena, você perdeu :( **\n' + \
			'*' * len('** Que pena, você perdeu :( **') + \
			'\n\nA palavra era: %s' % (self.palavra)

		print(self.alerta)


# Função Principal
def main():
	forca = Forca(ler_txt())
	input()

# Execução
if __name__ == '__main__':
	main()