const foodCards = document.getElementsByName("food-card");
const csrftoken = Cookies.get("csrftoken");

foodCards.forEach((foodCard) => {
  const food = foodCard.querySelector("#food");
  const numberOfLikes = foodCard.querySelector("#num-likes");
  const like = foodCard.querySelector("#like");
  let foodName = food.innerText;
  let likeStatus = localStorage.getItem(`${foodName} like status`);
  if (likeStatus === "regular" || likeStatus == null) {
    like.classList.add("fa-regular");
  }
  if (likeStatus === "solid") {
    like.classList.add(`fa-${likeStatus}`);
  }
  console.log(likeStatus);
  numberOfLikes.innerText =
    localStorage.getItem(foodName) > 0 ? localStorage.getItem(foodName) : "";
});

// numberOfLikes.innerText =
//   localStorage.getItem(foodName) > 0 ? localStorage.getItem(foodName) : "";

foodCards.forEach((foodCard) => {
  const like = foodCard.querySelector("#like");
  const food = foodCard.querySelector("#food");
  const numberOfLikes = foodCard.querySelector("#num-likes");
  let foodName = food.innerText;
  // let likeStatus = localStorage.getItem(`${foodName} like status`);
  like.addEventListener("click", () => {
    let data = { food_name: foodName };
    let options = {
      method: "POST",
      headers: {
        "Content-Type": "application/json;charset=utf-8",
        "X-CSRFTOKEN": csrftoken,
      },
      body: JSON.stringify(data),
    };
    fetch("http://127.0.0.1:8000/like-food/", options)
      .then((res) => res.json())
      .then((data) => {
        localStorage.setItem(foodName, data.food_likes);
        localStorage.setItem(`${foodName} like status`, data.like_status);
        let newLikeStatus = localStorage.getItem(`${foodName} like status`);
        console.log(newLikeStatus);
        let oldLikeStatus = newLikeStatus === "regular" ? "solid" : "regular";
        like.classList.remove(`fa-${oldLikeStatus}`);
        like.classList.add(`fa-${newLikeStatus}`);
        numberOfLikes.innerText =
          localStorage.getItem(foodName) > 0
            ? localStorage.getItem(foodName)
            : "";
      });
  });
});
