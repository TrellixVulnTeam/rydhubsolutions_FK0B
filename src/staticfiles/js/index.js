// window.$ = window.jQuery = require('jquery');
// going to load bootstrap using a link in my html so that it loads before this
// import 'bootstrap';
// import 'bootstrap/dist/css/bootstrap.min.css';
import Vue from 'vue';
// importing axios needs to be done on each component or mixin seperatly


// components from github
import Dropdown from 'bp-vuejs-dropdown';

import { Carousel, Slide } from "vue-carousel";
import "./css/vue-carousel.css"

// my custom components
import Navigation from "./components/navigation.vue";
import Checkout_script from "./components/checkout_script.vue";
import onload from "./components/onload.vue";


// mixins
import {base_global} from "./mixins/base_global.js"
import {vue_slides} from "./mixins/vue_slides.js"

// some random css
import "./css/random-css.css"

const app = new Vue({
    el: '#app',
    data: function(){
        return {

        }
    },
    delimiters: ["[[","]]"], //changing the default because thats what django's template language uses as well
    components: {
        Dropdown,
        Navigation,
        Checkout_script,
        onload,
        Carousel,
        Slide,

    },
    mixins: [base_global, vue_slides],
    
});