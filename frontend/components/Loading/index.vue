<template>
    <div class="w-full h-screen bg-[rgba(0,0,0,0.6)] backdrop-blur fixed top-0 left-0 z-50 flex flex-col justify-center items-center">
        <svg class="bounce" width="128" height="128" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" fill="white"><path d="M11.5 23l-8.5-4.535v-3.953l5.4 3.122 3.1-3.406v8.772zm1-.001v-8.806l3.162 3.343 5.338-2.958v3.887l-8.5 4.534zm-10.339-10.125l-2.161-1.244 3-3.302-3-2.823 8.718-4.505 3.215 2.385 3.325-2.385 8.742 4.561-2.995 2.771 2.995 3.443-2.242 1.241v-.001l-5.903 3.27-3.348-3.541 7.416-3.962-7.922-4.372-7.923 4.372 7.422 3.937v.024l-3.297 3.622-5.203-3.008-.16-.092-.679-.393v.002z"/></svg>
        <vue-typed-js class="text-white" :strings="['Patience ça chauffe ...', 'On déballe la marchandise ...', 'Prennez un café ça arrive ...', 'Le moteur se met en marche ...', 'Livraison de la marchandise en cours ...', 'Silence ça tourne ...' ]" :loop="true" :shuffle="true">
            <h1 class="typing text-xl select-none text-white"></h1>
        </vue-typed-js>
    </div>
</template>

<script>
export default {
    name: "LoadingComponent",
    data() {
        return {
            typed: undefined
        }
    },
}
</script>

<style scoped>
@keyframes bounce {
    0% {
        transform: translateY(0);
    }
    50% {
        transform: translateY(-15px);
    }
    100% {
        transform: translateY(0);
    }
}

.bounce {
    animation: bounce 4s ease-in infinite;
}
</style>
