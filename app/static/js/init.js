(function (){
    var root = document.documentElement;

    try {
        if (sessionStorage.getItem("msaLoaded")){
            root.classList.add("skip-loading");
        }

        var reduceMotion = window.matchMedia("(prefers-reduced-motion : reduce)").matches;
        if(sessionStorage.getItem("msaTransition") && !reduceMotion){
            root.classList.add("has-transition");
        }
    } catch (e){}
})();