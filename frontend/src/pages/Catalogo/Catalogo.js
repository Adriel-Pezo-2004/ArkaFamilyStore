import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import axios from 'axios';

const Catalogo = () => {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const location = useLocation();

  useEffect(() => {
    const fetchData = async () => {
      const params = new URLSearchParams(location.search);
      const term = params.get('search');
      setSearchTerm(term);

      if (!term) {
        setLoading(false);
        return;
      }

      try {
        console.log('Realizando búsqueda con término:', term);
        const response = await axios.get(`http://localhost:5000/api/search?search=${encodeURIComponent(term)}`);
        console.log('Datos recibidos:', response.data);
        
        if (Array.isArray(response.data)) {
          setResults(response.data);
        } else {
          console.error('La respuesta no es un array:', response.data);
          setResults([]);
        }
      } catch (err) {
        console.error('Error en la búsqueda:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [location.search]);

  if (loading) {
    return (
      <div className="container mx-auto p-4">
        <h2>Buscando productos...</h2>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto p-4">
        <h2>Error al buscar productos</h2>
        <p>{error}</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Resultados de la búsqueda: {searchTerm}</h1>
      
      {results.length === 0 ? (
        <p>No se encontraron productos para "{searchTerm}"</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {results.map((product) => (
            <div 
              key={product._id || Math.random()} 
              className="border rounded-lg p-4 shadow-md"
            >
              <img 
                src={product.imagen} 
                alt={product.nombre}
                className="w-full h-48 object-cover mb-4"
               
              />
              <h2 className="text-xl font-semibold mb-2">{product.nombre}</h2>
              <p className="text-gray-600 mb-2">{product.descripcion}</p>
              <p className="font-bold text-lg mb-2">${product.precio}</p>
              <p className="text-sm text-gray-500">Categoría: {product.categoria}</p>
            </div>
          ))}
        </div>
      )}
      
      <div className="mt-4">
        <p>Total de resultados: {results.length}</p>
      </div>
    </div>
  );
};

export default Catalogo;