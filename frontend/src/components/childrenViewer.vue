<template>
    <div>
        <div 
            class="viewer"
            v-if="instance"
        >
            <div 
                class="viewer-item" 
                v-for="(each, index) in instance" 
                :key="index"
            >
                <v-row>
                    <v-col cols=9>
                        <h3> <mrd-a :to="'/child/' + each.serial_number"> {{ each.name }} </mrd-a> </h3>
                        <p class="mb-1" > <span class="title"> MRecordID: </span> #{{ each.serial_number }}</p>
                        <p class="mb-1" > <span class="title"> День рождения </span> {{ each.birthday }}</p>
                        
                    </v-col>

                    <v-col cols=3 v-if="inputer">
                        <mrd-button @click="$emit('del', index)">
                            Удалить
                        </mrd-button>
                    </v-col>

                </v-row>


            </div>            
        </div>
    </div>
</template>

<script>
import mrdButton from '../components/mrdButton.vue'
import mrdA from '../components/mrdA.vue'

export default {
    components : { mrdButton, mrdA },
    props:{
        instance : {
            type : Array,
            required : true,
        },
        inputer : {
            type: Boolean,
            required: false,
            default: false,
        }
    },    
}
</script>

<style scoped>
.viewer-item{
    background-color: #A3B2CD;
    padding: 20px 15px;
    margin-bottom: 12px;
    box-sizing: border-box;
    color: #505050;
    font-weight: bold;
    border-radius: 7px;
    width: 100%;
    font-weight: bold;
}
.title{
    font-size: 14px;
    font-weight:300;
}
</style>