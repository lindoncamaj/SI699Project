import { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom"; // Import useNavigate

function Form() {
  const [minPrice, setMinPrice] = useState("");
  const [maxPrice, setMaxPrice] = useState("");
  const [location, setLocation] = useState("");
  const [carType, setCarType] = useState({
    sedan: false,
    suv: false,
    truck: false,
  });
  const [carMake, setCarMake] = useState([]);
  const [makes, setMakes] = useState([]);
  const [minMPG, setMinMPG] = useState([]);
  const [electric, setElectric] = useState([]);

  const navigate = useNavigate(); // Initialize navigation

  useEffect(() => {
    axios
      .get("http://localhost:8080/api/makes")
      .then((response) => {
        setMakes(response.data.data || []); // Store the "data" array from API response
      })
      .catch((err) => {
        console.error("API Error:", err);
      });
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log(minPrice, maxPrice, location, carMake, carType, minMPG, electric);

    // Validation check: Ensure all fields are filled
    if (!minPrice || !maxPrice || !location || !carMake || !electric || !Object.values(carType).includes(true) || !Object.values(electric).includes(true)) {
      alert("Please fill out all fields before submitting.");
      return;
    }

    const data = {
      minPrice,
      maxPrice,
      location,
      carType,
      carMake,
      minMPG
    };

    // Navigate to Recs page and pass form data
    axios.post("http://localhost:8080/recommend", data).then((response) => {navigate("/recs", {state: response.data})});
  };

  const handleCarTypeChange = (sub) => {
    setCarType((prev) => ({
      ...prev,
      [sub]: !prev[sub],
    }));
  };
  const handleElectric = (sub) => {
    setElectric((prev) => ({
      ...prev,
      [sub]: !prev[sub],
    }));
  };
  const handleReset = () => {
    // Reset all state variables here
    setMinPrice("");
    setMaxPrice("");
    setLocation("");
    setCarType({
      sedan: true,
      suv: false,
      truck: false,
    });
    setCarMake("");
  };
  return (
    <div className="Form">
      <h1>Match My Car</h1>
      <fieldset>
        <form action="#" method="get">
          <label htmlFor="minPrice">Minimum Price ($)*</label>
          <input
            type="number"
            name="minPrice"
            id="minPrice"
            value={minPrice}
            onChange={(e) => setMinPrice(e.target.value)}
            placeholder="Enter min price"
            required
          />
          <label htmlFor="maxPrice">Maximum Price ($)*</label>
          <input
            type="number"
            name="maxPrice"
            id="maxPrice"
            value={maxPrice}
            onChange={(e) => setMaxPrice(e.target.value)}
            placeholder="Enter max price"
            required
          />
          <label htmlFor="location">Location*</label>
          <input
            type="text"
            name="location"
            id="location"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            placeholder="Enter City or Zip Code"
            required
          />
          <label htmlFor="carType">Car Type*</label>
          <input
            type="checkbox"
            name="carType"
            id="sedan"
            checked={carType.sedan === true}
            onChange={(e) => handleCarTypeChange("sedan")}
          />
          Sedan
          <input
            type="checkbox"
            name="carType"
            id="suv"
            checked={carType.suv === true}
            onChange={(e) => handleCarTypeChange("suv")}
          />
          SUV
          <input
            type="checkbox"
            name="carType"
            id="truck"
            checked={carType.truck === true}
            onChange={(e) => handleCarTypeChange("truck")}
          />
          Truck
          <label>Car Make*</label>
          <select
            name="select"
            id="select"
            value={carMake}
            onChange={(e) => setCarMake(e.target.value)}
          >
            <option value="" disabled selected={carMake === ""}>
              Select an Option
            </option>

            {makes.map((make) => (
              <option key={make.id} value={make.name}>
                {make.name}
              </option>
            ))}
          </select>
          {/* <label htmlFor="electric">Electric?*</label> */}
          <input
            type="checkbox"
            name="electric"
            id="elec"
            checked={electric.elec === true}
            onChange={(e) => handleElectric("elec")}
          />
          Electric
          <input
            type="checkbox"
            name="electric"
            id="ice"
            checked={electric.ice === true}
            onChange={(e) => handleElectric("ice")}
          />
          ICE (Non-Electric)
          <input
            type="checkbox"
            name="electric"
            id="hybrid"
            checked={electric.hybrid === true}
            onChange={(e) => handleElectric("hybrid")}
          />
          Hybrid
          <label htmlFor="location">Fuel Economy (Optional)</label>
          <input
            type="text"
            name="minMPG"
            id="minMPG"
            value={minMPG}
            onChange={(e) => setMinMPG(e.target.value)}
            placeholder="Minimum MPG (Enter a number)"
            required
          />
          <button
            id="reset"
            type="reset"
            value="reset"
            onClick={() => handleReset()}
          >
            Reset
          </button>
          <button
            id="submit"
            type="submit"
            value="Submit"
            onClick={(e) => handleSubmit(e)}
          >
            Submit
          </button>
        </form>
      </fieldset>
    </div>
  );
}

export default Form;
