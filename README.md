# Degradação de imagens

Como erros de **ponto flutuante** podem destruir uma imagem?

Este projeto simula uma **máquina de precisão limitada** e mostra,
na prática, como operações numéricas introduzem distorções visuais **acumulativas**.


[comment]: <> (
TODO:
 varios gifs de degradação pra intuir o processo
)

# Simulando uma máquina pequena

## A classe Fl

O tipo _Fl_ é um modelo que simula o erro de representação de um ponto flutuante 
numa máquina de `b` **bits**, `t` dígitos de **mantissa** e **expoente** `k1 <= e <= k2`.

Ela simula as operações no espaço da máquina computando 

> `(A op B) = Fl( Fl(A) op Fl(B) )`

sendo `op` a sobrecarga dos principais operadores lógicos matemáticos usados na programação.

O modelo também tem features como **representação simbólica de valores infinitesimais** (_over_ / _underflow_ não corrompem o programa) e **representação na forma subnormal da mantissa** para maximizar o leque de representáveis, conforme feito em máquinas reais.


<img src="images/assets/reta_dos_representaveis.png" alt="reta dos representáveis" width="100%">


# Representando imagens com CV2 e NumPy

O **CV2** representa uma imagem como um array **NumPy** de _shape_ `(height, width, 4)` e _dtype_ `uint8`.

Isso pode ser entendido como uma matriz de `height` linhas e `width` colunas, 
onde cada elemento é um pixel (4-upla) com valores (`Blue`, `Green`, `Red`, `Alpha`)

<div style="display: flex; justify-content: space-around; align-items: center;">
<img src="images/assets/str_repr_gradiente.png" width="48%">
<img src="images/gradiente.png" width="48%">
</div>

Não é necessário converter os valores dos pixels para o tipo _Fl_, 
pois assumimos que a menor das máquinas consegue representar pelo menos os inteiros de 0 a 255. 

## Sistema de coordenadas geral

Todas as coordenadas desse programa usam o sistema `i j`, e não `x y`


# Manipulando imagens

Por questões de otimização, é feito o **fluxo inverso das transformações**: 
para cada elemento do contradomínio, aplica-se a transformação inversa para descobrir seu correspondente no domínio.

Isso evita a formação de gaps no contradomínio 
que deveriam ser preenchidos depois com a **interpolação** de forma redundante e trabalhosa.

Ao invés disso, o mapeamento reverso retorna uma **coordenada decimal**, 
que é então **interpolada** usando a função **parametrizada** escolhida 
(opções disponíveis no módulo `interp`).

[comment]: <> (
TODO:
diagrama mostrando o mapeamento inverson de uma imagem pra outra pela matriz inversa
)


## Transformações lineares

A função `linear_map` aplica uma dada matriz de transformação em uma imagem.

As funções `rotate` e `resize` são rotinas de nivel mais alto 
que **constroem a matriz** do `linear_map` a partir de **argumentos mais simples**, 
como um ângulo de rotação, uma nova largura em pixels e etc.

### Sistema de coordenadas para transformações lineares

Uma coordenada de uma imagem pode ter duas origens:
- **Origem da matriz** em que está contida
  - chamada de **pixel** 
- **Origem do plano cartesiano** em que está contida
  - chamada de **vetor**

[comment]: <> (
TODO: 
diagrama mostrando a mesma coordenada em sistemas diferentes
)

Esse sistema é necessário porque algumas transformações modificam o _bounding box_ da imagem, 
de forma que o valor na origem da matriz não se preserva (quebrando a linearidade).

[comment]: <> (
TODO: 
diagrama mostrando imagem transformada com origem fora da origem da matriz
)

Dessa forma, as operações lineares aplicadas devem usar as coordenadas do plano cartesiano, 
e não coordenadas de pixels em matrizes. 
Mas as coordenadas em pixels ainda são necessárias para ler e escrever valores na matriz.
**Por isso, o programa cambia matemáticamente entre esses sistemas de coordenadas nas operações.**

A ideia fundamental é que uma matriz enquadra uma imagem no plano cartesiano e,
ao fazer isso, **não é possível garantir que a origem do plano cartesiano está sobreposta com a origem da matriz**. 
Isso ocorre em todos os casos em que a imagem não está contida exclusivamente no 4° quadrante.

Por isso, para aplicar transformações em pixels, é preciso convertê-los para vetores no plano cartesiano antes.

Para **não corromper a linearidade**, as operações lineares desse programa seguem esse fluxo:

> `p` &harr; `v` &harr; `v'` &harr; `p'`


### Demo - Linear

<div style="display: flex; justify-content: space-around; align-items: center;">
<img src="images/tinycat.jpg" width="48%">
<img src="images/assets/transformed_tiny_cat.png" width="48%">
</div>
Aplicação de cisalhamento com reflexão horizontal


## Transformações não lineares com SymPy

A função `generic_map` aplica em uma imagem 
uma transformação genérica do tipo `f: R² -> R²` 
que é passada como `f(i,j) = g(i,j), h(i,j)` com `g, h: R² -> R¹`.

A biblioteca SymPy permite calcular a função inversa 
de quase qualquer composição de funções algébricas e trigonométricas,
e por isso foi usada para fazer o mapeamento do contradomínio para o domínio da imagem.

### Demo - Não Linear

<div style="display: flex; justify-content: space-around; align-items: center;">
<img src="images/cat.jpg" width="48%">
<img src="images/assets/cat_normal.png" width="48%">
</div>

Aplicação de `f(i,j) = [(i + sin( j/30 ) * ( j/5 )), j]`

# Análise de erros de representação: aplicando transformações com o tipo Fl

Comparações feitas entre `Float` nativo do Python e `Fl(b=10, t=1,  k1=-3, k2=3)`

## Transformações lineares








### Contração
`factor = 0.1`
`interpolation = bicubic`

`img:`

<img src="images/gam.jpg" width="100%">

#### Python Float

<img src="images/assets/gam_resized.png" width="100%">


[//]: # (#### Fl&#40;10, 2, -3, 3&#41;)

[//]: # ()
[//]: # (<div style="display: flex; justify-content: space-around; align-items: center;">)

[//]: # (<img src="images/gam_resized_fl_2.png" width="100%">)

[//]: # (</div>)

#### Fl

<div style="display: flex; justify-content: space-around; align-items: center;">
<img src="images/assets/gam_resized_fl.png" width="100%">
</div>






### Magnificação
`factor = 4`
`interpolation = bicubic`

`img:`

<img src="images/tinycat.jpg" width="100%">

#### Python Float

<img src="images/assets/tinycat_resized.png" width="100%">


#### Fl

<div style="display: flex; justify-content: space-around; align-items: center;">
<img src="images/assets/tinycat_resized_fl.png" width="100%">
</div>









### Deformação
```
matrix = [
    [-1, 0],
    [1, 2]
] 
```

`interpolation = bicubic`

`img:`

<img src="images/tinycat2.jpg" width="100%">

#### Python Float

<img src="images/assets/tinycat2_transformed.png" width="100%">


#### Fl

<div style="display: flex; justify-content: space-around; align-items: center;">
<img src="images/assets/tinycat2_transformed_fl.png" width="100%">
</div>








### Rotação

`angle = 150°`
`interpolation = bicubic`

`img:`

<img src="images/cat.jpg" width="100%">

#### Python Float

<img src="images/assets/cat_rotated.png" width="100%">


#### Fl

<div style="display: flex; justify-content: space-around; align-items: center;">
<img src="images/assets/cat_rotated_fl.png" width="100%">
</div>






### Cópias repetidas




#### Decomposição de contração em multiplas contrações consecutivas

`factor = (0.1)^(1/9)`
`interpolation = bicubic`


##### Python Float

<div style="display: flex; justify-content: space-around; align-items: center;">
<img src="images/assets/0_gam_contracted.png" width="33%">
<img src="images/assets/1_gam_contracted.png" width="33%">
<img src="images/assets/2_gam_contracted.png" width="33%">
</div>

<div style="display: flex; justify-content: space-around; align-items: center;">
<img src="images/assets/3_gam_contracted.png" width="33%">
<img src="images/assets/4_gam_contracted.png" width="33%">
<img src="images/assets/5_gam_contracted.png" width="33%">
</div>

<div style="display: flex; justify-content: space-around; align-items: center;">
<img src="images/assets/6_gam_contracted.png" width="33%">
<img src="images/assets/7_gam_contracted.png" width="33%">
<img src="images/assets/8_gam_contracted.png" width="33%">
</div>

<img src="images/assets/9_gam_contracted.png" width="100%">


##### Fl

<div style="display: flex; justify-content: space-around; align-items: center;">
<img src="images/assets/0_gam_contracted_fl.png" width="33%">
<img src="images/assets/1_gam_contracted_fl.png" width="33%">
<img src="images/assets/2_gam_contracted_fl.png" width="33%">
</div>

<div style="display: flex; justify-content: space-around; align-items: center;">
<img src="images/assets/3_gam_contracted_fl.png" width="33%">
<img src="images/assets/4_gam_contracted_fl.png" width="33%">
<img src="images/assets/5_gam_contracted_fl.png" width="33%">
</div>

<div style="display: flex; justify-content: space-around; align-items: center;">
<img src="images/assets/6_gam_contracted_fl.png" width="33%">
<img src="images/assets/7_gam_contracted_fl.png" width="33%">
<img src="images/assets/8_gam_contracted_fl.png" width="33%">
</div>

<img src="images/assets/9_gam_contracted_fl.png" width="100%">




#### Decomposição de magnificação em multiplas magnificações consecutivas

#### Decomposição de deformação em multiplas deformações consecutivas





#### Decomposição de rotação em múltiplas rotações consecutivas

`angle = 10°`
`interpolation = bicubic`



##### Python Float

<div style="display: flex; justify-content: space-around; align-items: center;">
<img src="images/assets/0gam_rotated.png" width="33%">
<img src="images/assets/1gam_rotated.png" width="33%">
<img src="images/assets/2gam_rotated.png" width="33%">
</div>

<div style="display: flex; justify-content: space-around; align-items: center;">
<img src="images/assets/3gam_rotated.png" width="33%">
<img src="images/assets/4gam_rotated.png" width="33%">
<img src="images/assets/5gam_rotated.png" width="33%">
</div>

<div style="display: flex; justify-content: space-around; align-items: center;">
<img src="images/assets/6gam_rotated.png" width="33%">
<img src="images/assets/7gam_rotated.png" width="33%">
<img src="images/assets/8gam_rotated.png" width="33%">
</div>


##### Fl

<div style="display: flex; justify-content: space-around; align-items: center;">
<img src="images/assets/0gam_rotated_fl.png" width="24%">
<img src="images/assets/1gam_rotated_fl.png" width="24%">
<img src="images/assets/2gam_rotated_fl.png" width="24%">
<img src="images/assets/3gam_rotated_fl.png" width="24%">
</div>

<div style="display: flex; justify-content: space-around; align-items: center;">
<img src="images/assets/4gam_rotated_fl.png" width="24%">
<img src="images/assets/5gam_rotated_fl.png" width="24%">
<img src="images/assets/6gam_rotated_fl.png" width="24%">
<img src="images/assets/7gam_rotated_fl.png" width="24%">
</div>

<div style="display: flex; justify-content: space-around; align-items: center;">
<img src="images/assets/8gam_rotated_fl.png" width="24%">
<img src="images/assets/9gam_rotated_fl.png" width="24%">
<img src="images/assets/10gam_rotated_fl.png" width="24%">
<img src="images/assets/11gam_rotated_fl.png" width="24%">
</div>

<div style="display: flex; justify-content: space-around; align-items: center;">
<img src="images/assets/12gam_rotated_fl.png" width="24%">
<img src="images/assets/13gam_rotated_fl.png" width="24%">
<img src="images/assets/14gam_rotated_fl.png" width="24%">
<img src="images/assets/15gam_rotated_fl.png" width="24%">
</div>



#### Composições transformação-inversão


## Transformações não lineares

