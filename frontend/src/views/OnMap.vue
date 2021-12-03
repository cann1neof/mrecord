<template>
    <div>
        <div class="mt-3">
            <h1 class="main-title">Наши партнеры </h1>
        </div>
        <div style="width: 60vw;" class="mx-auto mb-3">
           Если пользователь наблюдается в одной из больниц-партнеров (не важно – амбулаторно или стационарно), то у него будет возможность автоматически сохранять в системе информацию о приемах. Врачи больниц-партнеров во время приема смогут получать указанную пользователем информацию, например, историю болезни, изменять ее и анализировать. Для всего этого разработано специальное приложение - MRecord Hospital Assistant. Все больницы, желающие пользоваться системой, могут заполнить специальную форму.
        </div>
        <div
        style="width:100vw; height:60vh;" 
        class="mx-0 px-0"
        >
            <yandex-map
            :zoom="10"
            :coords="[55.74954, 37.621587]"
            map-type="map"
            :settings="mapSettings"
            style="width: 100%; height: 100%;"
            :controls="['zoomControl']"
            >
                <ymap-marker
                v-for="(item, index) of markers"
                marker-type="Placemark"
                :key="index"
                :coords="item.coords"
                :marker-id="index"
                :balloon-template="balloonTemplate(item)"
                >

                </ymap-marker>
            </yandex-map>
        </div>

        <div class="my-3">
            <h2 class="main-title"> Вы хотите подключить свою больницу к системе? Заполните форму и с вам обязательно свяжутся! </h2>
            <div style="width:167px" class="mx-auto">
                <mrd-button to="/newpartner/" dark>Присоединиться!</mrd-button>
            </div>
        </div>
    </div>
</template>

<script>
import mrdButton from '../components/mrdButton.vue'
export default {
    data: () => ({
        mapSettings: {
            apiKey: '0743cdc0-0634-4b6f-be02-c546c5add538',
            lang: 'ru_RU',
            coordorder: 'latlong',
            version: '2.1'
        },
        markers: [],
    }),
    components: {
        mrdButton
    },
    methods: {
        getCoords(e){
            this.coords = e.get('coords')
        },
        balloonTemplate({headline, text}) {
        return `
            <p><b> ${headline}</b> <br /> ${text}</p>
        `
        },
        getMarkers(){
            const url = this.$store.getters.url + 'markers/partners/'
            this.$axios.get(url).then(res=>{
                this.markers = res.data
                console.log(this.markers)
            }).catch( () => {
                this.$emit('raise', {errCode: 'SM01', errMessage: 'Ошибка при загрузке данных карты, попробуйте снова'})
            })
        },
    },
    watch:{
        $route(){
            this.getMarkers()
        }
    },
    mounted(){
        this.getMarkers()
    },

}
</script>

<style scoped>
.main-title{
    font-size: 30px;
    color: #404040;
}
</style>