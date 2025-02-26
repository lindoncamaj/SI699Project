import { useLocation } from "react-router-dom";

const Recs = () => {
  const location = useLocation();
  const formData = location.state || {}; // Get form data from state

  const selectedCarTypes = Object.keys(formData.carType)
    .filter((type) => formData.carType[type]) // Get only selected types
    .map((type) => type.charAt(0).toUpperCase() + type.slice(1)); // Capitalize first letter

  return (
    <div>
      <h1>Recommendations</h1>
      <p>
        <strong>Min Price:</strong> {formData.minPrice}
      </p>
      <p>
        <strong>Max Price:</strong> {formData.maxPrice}
      </p>
      <p>
        <strong>Location:</strong> {formData.location}
      </p>
      <p>
        <strong>Car Type:</strong>{" "}
        {selectedCarTypes.length > 0 ? selectedCarTypes.join(", ") : "None"}
      </p>
      <p>
        <strong>Car Make:</strong> {formData.carMake}
      </p>
    </div>
  );
};

export default Recs;
