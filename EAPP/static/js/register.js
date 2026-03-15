document.getElementById("registration-form").addEventListener("submit", async (event) => {
    event.preventDefault();
  
    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const address = document.getElementById("address").value;
    const userType = document.getElementById("user-type").value;
    const userAID = document.getElementById("user-aid").value;
  
    const response = await fetch('/api/users', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        User_Fullname: name,
        User_Email: email,
        User_Password_Hash: password,
        User_Address: address,
        User_Type: userType,
        User_AID: userAID,
      }),
    });
  
    const result = await response.json();
  
    if (response.ok) {
      // ✅ Store user_id for later cart operations
      localStorage.setItem('user_id', result.User_Id);
  
      alert('Registration successful!');
      window.location.href = '/login';
    } else {
      alert(`Registration failed: ${result.error}`);
    }
  });