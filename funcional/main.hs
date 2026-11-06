module Main where

import Data.List (minimumBy)
import Data.Ord (comparing)

type Vertice   = String
type Distancia = Double
type Pedagio   = Double
type Aresta    = (Vertice, Vertice, Distancia, Pedagio)
type Trajeto   = [Vertice]

data Status = ROTA_ENCONTRADA 
            | ROTA_INEXISTENTE 
            | ORCAMENTO_INSUFICIENTE 
            | ENTRADA_INVALIDA 
            deriving (Show, Eq)

data Resultado = Resultado {
    status         :: Status,
    caminho        :: Trajeto,
    distanciaTotal :: Double,
    custoTotal     :: Double
} deriving (Show, Eq)

-- busca recursiva de caminhos evitando ciclos
buscarCaminhos :: [Aresta] -> Vertice -> Vertice -> [Vertice] -> Double -> Double -> [([Vertice], Double, Double)]
buscarCaminhos arestas atual destino visitados distAcc custoAcc
    | atual == destino = [(trajetoAtual, distAcc, custoAcc)]
    | otherwise = 
        concat [ buscarCaminhos arestas v destino trajetoAtual (distAcc + d) (custoAcc + p)
               | (u, v, d, p) <- arestas
               , u == atual
               , v `notElem` trajetoAtual ]
  where
    trajetoAtual = visitados ++ [atual]

-- valida entradas, busca caminhos, filtra orcamento e escolhe a menor rota
planejarRota :: [Aresta] -> Vertice -> Vertice -> Double -> Resultado
planejarRota arestas origem destino orcamento
    | null arestas || orcamento < 0 = 
        Resultado ENTRADA_INVALIDA [] 0.0 0.0
    | origem `notElem` todosVertices || destino `notElem` todosVertices = 
        Resultado ENTRADA_INVALIDA [] 0.0 0.0
    | null caminhosPossiveis = 
        Resultado ROTA_INEXISTENTE [] 0.0 0.0
    | null validosOrcamento = 
        Resultado ORCAMENTO_INSUFICIENTE [] 0.0 0.0
    | otherwise = 
        let (melhorTrajeto, melhorDist, melhorCusto) = 
                minimumBy (comparing (\(t, d, c) -> (d, c, t))) validosOrcamento
        in Resultado ROTA_ENCONTRADA melhorTrajeto melhorDist melhorCusto
  where
    todosVertices = concat [ [u, v] | (u, v, _, _) <- arestas ]
    caminhosPossiveis = buscarCaminhos arestas origem destino [] 0.0 0.0
    validosOrcamento = filter (\(_, _, c) -> c <= orcamento) caminhosPossiveis

-- dados de exemplo para teste
malhaTeste :: [Aresta]
malhaTeste = 
    [ ("A", "B", 10.0, 5.0)
    , ("A", "C", 15.0, 0.0)
    , ("B", "D", 10.0, 5.0)
    , ("C", "D", 12.0, 2.0)
    , ("D", "E", 8.0, 3.0)
    ]

main :: IO ()
main = do
    putStrLn "Etapa 06 - Haskell"
    
    let res1 = planejarRota malhaTeste "A" "D" 15.0
    putStrLn "Teste 1 (orcamento suficiente):"
    print res1

    let res2 = planejarRota malhaTeste "A" "D" 2.0
    putStrLn "Teste 2 (orcamento insuficiente):"
    print res2
