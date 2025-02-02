import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Swal from 'sweetalert2';
import './Home.css';

const Home = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const navigate = useNavigate();

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    const term = searchTerm.trim();
    
    if (term) {
      console.log('Navegando a búsqueda con término:', term);
      navigate(`/catalogo?search=${encodeURIComponent(term)}`);
    } else {
      Swal.fire({
        icon: 'error',
        title: 'Oops...',
        text: 'Por favor ingrese un término de búsqueda!',
      });
    }
  };

  return (
    <div className="container mx-auto p-4">  
      <form onSubmit={handleSearchSubmit} className="max-w-md mx-auto">
        <h1 className="text-3xl font-bold mb-8">ARKA FAMILY STORE</h1>
        <div className="flex gap-2">
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Buscar productos..."
            className="flex-1 p-2 border rounded"
            required
          />
          <button 
            type="submit"
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          >
            Buscar
          </button>
        </div>
      </form>
    </div>
  );
};

export default Home;