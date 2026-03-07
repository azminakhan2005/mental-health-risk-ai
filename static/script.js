function toggleChat() {

    const box = document.getElementById("chatBox");

    if (box.style.display === "flex") {
        box.style.display = "none";
    } else {
        box.style.display = "flex";
    }
}


async function sendMessage(){

    const input = document.getElementById("chatInput");
    const message = input.value.trim();
    if(!message) return;

    const chat = document.getElementById("chatMessages");

    // USER MESSAGE
    chat.innerHTML += `
        <div class="user-msg">${message}</div>
    `;

    input.value = "";

   
    chat.scrollTop = chat.scrollHeight;

    const res = await fetch("/chat",{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({message:message})
    });

    const data = await res.json();


    // BOT MESSAGE
    chat.innerHTML += `
        <div class="bot-msg">${data.reply}</div>
    `;

    chat.scrollTop = chat.scrollHeight;
}
document.getElementById("chatInput").addEventListener("keypress", function(e){
    if(e.key === "Enter"){
        sendMessage();
    }
});