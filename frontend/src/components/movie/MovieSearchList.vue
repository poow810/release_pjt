<template>
    <div>
        <p>{{ props }}</p>
    </div>
</template>

<script setup>

const props = defineProps({
    searchMovie: Object
})
</script>