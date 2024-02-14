

function getPosts(){

    let url = "http://localhost:8000/posts"

    let options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            // other headers as needed
        },
        body: JSON.stringify(data), // data to be sent in the request body
    }
    
    fetch(url, options) 
    .then(response => {
        if(!response.ok){
            console.log(response)
            throw new Error("cant connect")
        }
        return response.json()
    })
    .then(data => {
        console.log(data)
        document.getElementById("ok").innerHTML = data.message
    })
    .catch(err => {
        document.getElementById("ok").innerHTML = "Something went wrong"
        console.error("err")
    })

    
}


getPosts()