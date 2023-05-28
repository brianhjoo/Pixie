import { useEffect, useState } from "react";
import PixieAPI from "./api";


function App() {
  const [countries, setCountries] = useState([]);
  const [errors, setErrors] = useState(null);

  useEffect(function fetchCountriesOnMount() {
    async function getCountries() {
      try {
        const countries = await PixieAPI.getCountries();
        setCountries(countries);
      } catch(err) {
          setErrors(err);
      }
    }
    getCountries();
  }, []);

  if (errors) return 'Something went wrong!';

  return (
    <ul className="m-6">
      {countries.map((country) => (
        <li key={country.name} className="text-blue-500">{country.name}</li>
      ))}
    </ul>
  );
}

export default App;