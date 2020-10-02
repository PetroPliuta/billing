let timer = 0;
const list1 = [...document.getElementsByTagName("input")];
list1.forEach((element) => {
  //   console.log(element.type);
  if (element.type == "password") {
    element.addEventListener("mouseenter", (ev) => {
      timer = setTimeout(() => {
        element.type = "text";
      }, 3000);
    });
    element.addEventListener("mouseleave", (ev) => {
      if (timer) {
        clearTimeout(timer);
        timer = 0;
      }
    });
  }
});
