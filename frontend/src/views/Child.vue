<template>
    <div>
        <v-row class="mx-auto" v-if="show">
            <v-col cols=4 :class="getCotainerClass"> 
                <h2 class="main-title">
                    Персональная информация
                </h2>
                <v-card width="50vw" class=" mx-auto pa-5" color="#013AAA" dark>
                    <h3> <span class="cont-title" > Имя: </span> {{ last_name }} {{ first_name }} {{ second_name }}</h3>
                    <h3> <span class="cont-title" > MRecord id: </span> #{{ id }} </h3>
                    <h3> <span class="cont-title" > Страховой номер: </span> {{ insurance_number }} </h3>
                    <h3> <span class="cont-title" > Группа крови: </span>{{ blood_type }}</h3>
                    <h3> <span class="cont-title" > День рождения: </span>{{ birthday }}</h3>
                    <mrd-button dark class="mt-2" :to="`/child/${id}/settings/`" color="#D96906">
                        <v-icon> mdi-cog-outline </v-icon> Настройки
                    </mrd-button>
                </v-card>

                <v-card v-if="hospitals[0]" width="50vw" class=" mx-auto mt-3 pa-5" color="#013AAA" dark>
                    <span class="cont-title"> Последние посещения врача </span>
                    <hospitals-viewer :inputer="false" :instance="hospitals" ></hospitals-viewer>
                </v-card>

                <v-card v-if="recipes[0]" width="50vw" class=" mx-auto mt-3 pa-5" color="#013AAA" dark>
                    <span class="cont-title"> Лекарства и процедуры </span>
                    <recipes-viewer :inputer="false" :instance="recipes" ></recipes-viewer>
                </v-card>
                        
            </v-col>

            <v-col cols=8 v-if="illnesses[0]">
                <h2 class="main-title">
                    Заболевания и противопоказания
                </h2>
                <v-card width="100%" class="pa-5" color="#013AAA" dark>
                    <illnesses-viewer :inputer="false" :instance="illnesses" ></illnesses-viewer>
                </v-card>
            </v-col>
        </v-row>
    </div>
</template>

<script>
import mrdButton from '../components/mrdButton.vue'
import recipesViewer from '../components/recipesViewer.vue'
import illnessesViewer from '../components/illnessesViewer.vue'
import hospitalsViewer from '../components/hospitalsViewer.vue'

export default {
    components : {
        mrdButton,
        recipesViewer,
        illnessesViewer,
        hospitalsViewer,
    },
    props: ['id'],
    data: ()=>({
        last_name : '',
        first_name : '',
        second_name : '',
        insurance_number : '',
        blood_type : '',
        hospitals : [],
        recipes : [],
        illnesses : [],
        birthday : '',
        show : false,

    }),
    methods: {
        async loadData(){
            const url = this.$store.getters.url + 'octopus/' + this.$store.getters.token + '/c/?id=' + this.id
            await this.$axios.get(url)
                .then(res => {
                    console.log(res.data)
                    this.show = this.updateData(res.data)
                }).catch(err => {
                    console.log(err)
                })
        },
        updateData(data){
            this.last_name = data.last_name 
            this.first_name = data.first_name 
            this.second_name = data.second_name 
            this.insurance_number = data.insurance_number 
            this.blood_type = data.blood_type 
            this.birthday = data.birthday 
            this.hospitals = data.hospitals != [] ? JSON.parse(data.hospitals) : []
            this.recipes   = data.recipes != [] ? JSON.parse(data.recipes) : []
            this.illnesses = data.illnesses != [] ? JSON.parse(data.illnesses) : []

            return true
        }
    },
    computed: {
        getCotainerClass(){
            if(!this.illnesses[0]){
                return { 'mx-auto' : true }
            } else {
                return { 'mx-auto' : false }
            }
        },
    },
    watch: {
        $route(){
            if (!this.$store.getters.status)
                this.$router.push('/login')
            else this.loadData()
        },
    },
    mounted(){
        if (!this.$store.getters.status)
            this.$router.push('/login')
        else this.loadData()
    }

}

</script>

<style scoped>
.container{
    background-color: #A3B2CD;
    padding: 20px 15px;
    margin-bottom: 12px;
    box-sizing: border-box;
    color: #505050;
    font-weight: bold;
    border-radius: 7px;
}
.cont-title{
    font-size: 14px;
    font-weight: 300;
}
.block-title{
    font-weight: bolder;
    color: #505050;
}
.main-title{
    font-size: 30px;
    font-weight:900;
    color: #404040;
}
</style>
