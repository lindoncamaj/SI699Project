import { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom"; // Import useNavigate
import Select from "react-select";
import { useAuth } from '../context/AuthContext'; // Import the useAuth hook
import LoadingScreen from "./LoadingScreen";

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
  const [minMPG, setMinMPG] = useState(0);
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

  const navigate = useNavigate(); // Initialize navigation
  const { isLoggedIn, logout } = useAuth(); // Use authentication state and functions from context
  const [loading, setLoading] = useState(false);

  // const [user, setUser] = useState(null);
  // const [loading, setLoading] = useState(true);
  // const [error, setError] = useState(null);

  useEffect(() => {
    const checkSession = async () => {
      try {
        const response = await axios.get("http://0.0.0.0:8080/session", {
          withCredentials: true,
        });
        if (!response.data.logged_in) {
          logout(); // If not logged in, call logout to update context
        }
        // If you do something on logged in status, manage within context
      } catch (error) {
        console.error("Error checking session:", error);
        logout();
      }
    };

    checkSession();
  }, [logout]);

  const handleLogin = () => {
    navigate("/login"); // Redirect to the login page
  };

  const handleLogout = async () => {
    try {
      await axios.post(
        "http://0.0.0.0:8080/logout",
        {},
        { withCredentials: true }
      );
      logout(); // Call logout from context
    } catch (error) {
      console.error("Logout error:", error);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log(
      minPrice,
      maxPrice,
      location,
      carMake,
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
      electric,
      drivetrain,
      minMPG,
    };

    setLoading(true);

    // Navigate to Recs page and pass form data
    axios
      .post("http://0.0.0.0:8080/recommend", data, { withCredentials: true })
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
    <div className="Form">
      <h1>Match My Car</h1>
      <button onClick={isLoggedIn ? handleLogout : handleLogin}>
        {isLoggedIn ? "Logout" : "Login"}
      </button>

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
          Front Wheel Drive
          <input
            type="checkbox"
            name="drivetrain"
            id="rwd"
            checked={drivetrain.rwd === true}
            onChange={(e) => handleDrivetrain("rwd")}
          />
          Rear Wheel Drive
          <input
            type="checkbox"
            name="drivetrain"
            id="awd"
            checked={drivetrain.awd === true}
            onChange={(e) => handleDrivetrain("awd")}
          />
          All Wheel Drive
          {/* MPG INPUT */}
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
