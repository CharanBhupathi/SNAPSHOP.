async function loginUser() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
  
    const response = await fetch('/api/users/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        User_Email: email,
        User_Password_Hash: password,
      })
    });
  
    const result = await response.json();
  
    if (response.ok) {
      // ✅ Store user_id and session token in localStorage
      localStorage.setItem('user_id', result.User_Id);
      localStorage.setItem('sessionToken', `Bearer ${result.User_Id}`);
  
      alert(result.message);
      window.location.href = '/categories';
    } else if (response.status === 404) {
      alert(result.error);
      window.location.href = '/register';
    } else {
      alert(result.error);
    }
  }