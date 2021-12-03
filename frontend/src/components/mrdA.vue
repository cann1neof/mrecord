<template>
    <a @click=" to ? $router.push(to) : $emit('click')"> 
        <slot> </slot>
    </a>
</template>

<script>
    export default {
        props:['to']
    }
</script>

<style>
</style>