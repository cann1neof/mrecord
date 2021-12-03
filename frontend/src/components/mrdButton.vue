<template>
    <v-btn
        :to="to"
        :color="color ? color : '#0040c0'"
        :class = "textColor"
        :type = "type"
        @click="$emit('click')"
    >
        <slot></slot>
    </v-btn>
</template>

<script>
export default {
    props : ['to', "color", "light", "dark", "big", "type", 'ltl', 'halfLeft', 'halfRight'], 
    computed : {
        textColor(){
            const output = {
                    'mrd-button' : true,
                    'mrd-text-color-dark' : false, 
                    'mrd-text-color-light' : false, 
                    'mrd-font-big' : false,
                    'mrd-font-ltl' : false,
                    'left-oriented' : false,
                    'right-oriented' : false,
            }
            if(this.light === ""){
                output['mrd-text-color-dark'] = true
            }
            if(this.dark === ""){
                output['mrd-text-color-light'] = true
            }
            if(this.big === ""){
                output['mrd-font-big'] = true
            }
            if(this.ltl === ""){
                output['mrd-font-ltl'] = true
            }
            if(this.halfLeft === ""){
                output['left-oriented'] = true
            }
            if(this.halfRight === ""){
                output['right-oriented'] = true
            }
            return output
        }
    }
}
</script>

<style>
.mrd-button{
    min-width: 100px;
    height: 50px;
    border-radius: 17px !important;
    box-shadow: none !important;
    text-transform: none !important;
}
.mrd-text-color-dark > span{
    color: #000;
}
.mrd-text-color-light > span{
    color: #fff;
}

.mrd-font-big {
    height: 60px !important;
    padding: 0 30px !important;
}

.mrd-font-big > span{
    font-size: 24px;
}
.mrd-font-ltl{
    height: 35px !important;
    padding: 2 10px !important;
}

.mrd-font-ltl > span {
    font-size: 10px;
}

.left-oriented{
    min-width: 50px;
    border-top-left-radius: 17px !important;
    border-bottom-left-radius: 17px !important;
    border-top-right-radius: 0px !important;
    border-bottom-right-radius: 0px !important;
}

.right-oriented{
    min-width: 50px;
    border-top-left-radius: 0px !important;
    border-bottom-left-radius: 0px !important;
    border-top-right-radius: 17px !important;
    border-bottom-right-radius: 17px !important;
}
</style>
