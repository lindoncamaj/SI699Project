import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Select from "react-select";
import axios from "axios";
import LoadingScreen from "./LoadingScreen";

function Form() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  const [minPrice, setMinPrice] = useState("");
  const [maxPrice, setMaxPrice] = useState("");
  const [location, setLocation] = useState("");
  const [carType, setCarType] = useState({
    sedan: false,
    suv: false,
    truck: false,
  });
  const [carMake, setCarMake] = useState([]);
  const makes = [
    { value: "1", label: "Acura" },
    { value: "2", label: "Audi" },
    { value: "3", label: "BMW" },
    { value: "4", label: "Buick" },
    { value: "5", label: "Cadillac" },
    { value: "6", label: "Chevrolet" },
    { value: "7", label: "Chrysler" },
    { value: "8", label: "Dodge" },
    { value: "9", label: "Ford" },
    { value: "10", label: "Genesis" },
    { value: "11", label: "GMC" },
    { value: "12", label: "Honda" },
    { value: "13", label: "Hyundai" },
    { value: "14", label: "Infiniti" },
    { value: "15", label: "Jeep" },
    { value: "16", label: "Kia" },
    { value: "17", label: "Lincoln" },
    { value: "18", label: "Mazda" },
    { value: "19", label: "Mercedes-Benz" },
    { value: "20", label: "Mitsubishi" },
    { value: "21", label: "Nissan" },
    { value: "22", label: "Subaru" },
    { value: "23", label: "Tesla" },
    { value: "24", label: "Toyota" },
    { value: "25", label: "Volkswagen" },
    { value: "26", label: "Volvo" },
  ];
  const[carYear, setCarYear] = useState(2010);
  const years = [
    { value: 2010, label: 2010 },
    { value: 2011, label: 2011 },
    { value: 2012, label: 2012 },
    { value: 2013, label: 2013 },
    { value: 2014, label: 2014 },
    { value: 2015, label: 2015 },
    { value: 2016, label: 2016 },
    { value: 2017, label: 2017 },
    { value: 2018, label: 2018 },
    { value: 2019, label: 2019 },
    { value: 2020, label: 2020 },
    { value: 2021, label: 2021 },
    { value: 2022, label: 2022 },
    { value: 2023, label: 2023 },
    { value: 2024, label: 2024 },
  ]
  const [electric, setElectric] = useState({
    elec: false,
    gas: false,
    hybrid: false,
  });
  const [drivetrain, setDrivetrain] = useState({
    fwd: false,
    rwd: false,
    awd: false,
  });
  const [minMPG, setMinMPG] = useState(0);

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log(
      minPrice,
      maxPrice,
      location,
      carMake,
      carYear,
      carType,
      minMPG,
      electric,
      drivetrain
    );

    // Validation check: Ensure all fields are filled
    if (
      !minPrice ||
      !maxPrice ||
      !location ||
      !carMake ||
      !carYear ||
      !Object.values(drivetrain).includes(true)  ||
      !Object.values(carType).includes(true) ||
      !Object.values(electric).includes(true)
    ) {
      alert("Please fill out all required fields before submitting.");
      return;
    }

    const data = {
      minPrice,
      maxPrice,
      location,
      carType,
      carMake,
      carYear,
      electric,
      drivetrain,
      minMPG,
    };

    setLoading(true);

    // Navigate to Recs page and pass form data
    axios
      .post("http://127.0.0.1:8080/recommend", data, { withCredentials: true })
      .then((response) => {
        navigate("/recs", { state: response.data });
      })
      .catch((error) => {
        console.error("Error loading page:", error);
        setLoading(false); // hide on error
      });
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
  const handleDrivetrain = (sub) => {
    setDrivetrain((prev) => ({
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
    setCarYear(2010);
    setDrivetrain({
      fwd: false,
      rwd: false,
      awd: false,
    });
    setElectric({
      elec: false,
      gas: false,
      hybrid: false,
    });
    setMinMPG(0);
  };
  return loading ? (
    <LoadingScreen />
  ) :  (
    <div>
      <h1>Find My Car</h1>

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
            placeholder="Enter Zip Code"
            required
          />
          {/* CAR TYPE CHECKBOX */}
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
          {/* CAR MAKE DROPDOWN */}
          <label>Car Make*</label>
          <Select
            name="select"
            id="select"
            isMulti
            options={makes}
            value={carMake}
            onChange={(e) => setCarMake(e)}
          />
          <label>Minimum Car Year*</label>
          <Select
            name="year"
            id="select"
            options={years}
            value={carYear}
            onChange={(e) => setCarYear(e)}
          />
          {/* ELECTRIC/GAS/HYBRID CHECKBOX */}
          <label>Electric/Gas/Hybrid*</label>
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
            id="gas"
            checked={electric.gas === true}
            onChange={(e) => handleElectric("gas")}
          />
          Traditional Gas
          <input
            type="checkbox"
            name="electric"
            id="hybrid"
            checked={electric.hybrid === true}
            onChange={(e) => handleElectric("hybrid")}
          />
          Hybrid
          {/* DRIVETRAIN CHECKBOX */}
          <label>Drivetrain*</label>
          <input
            type="checkbox"
            name="drivetrain"
            id="fwd"
            checked={drivetrain.fwd === true}
            onChange={(e) => handleDrivetrain("fwd")}
          />
          FWD
          <input
            type="checkbox"
            name="drivetrain"
            id="rwd"
            checked={drivetrain.rwd === true}
            onChange={(e) => handleDrivetrain("rwd")}
          />
          RWD
          <input
            type="checkbox"
            name="drivetrain"
            id="awd"
            checked={drivetrain.awd === true}
            onChange={(e) => handleDrivetrain("awd")}
          />
          AWD
          {/* MPG INPUT */}
          <label htmlFor="location">Minimum MPG (Optional)</label>
          <input
            type="text"
            name="minMPG"
            id="minMPG"
            value={minMPG}
            onChange={(e) => setMinMPG(e.target.value)}
            placeholder="Minimum MPG (Enter a number)"
            required
          />
          {/* RESET BUTTON */}
          <button
            id="reset"
            type="reset"
            value="reset"
            onClick={() => handleReset()}
          >
            Reset
          </button>
          {/* SUBMIT BUTTON */}
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
