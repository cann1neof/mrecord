<template>
    <div>
        <div class="triangle back"></div>
        <div class="par back">
            <slot> </slot>
        </div>
    </div>
</template>

<script>
    export default {
        
    }
</script>

<style>
.triangle {
	height: 0;
    width: 100vw;
    border-bottom: 130px solid #013AAA;
    border-left: 100vw solid transparent;
}
.par {
    width: 100vw;
    padding: 5vh 2vw;
    background-color: #013AAA;
    color: #fff;
}
.back{
    margin-left:-12px;
}
</style>