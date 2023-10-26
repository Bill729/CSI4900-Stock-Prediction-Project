<template>
    <div>
        <p>{{ msg }}</p>
        <div class="d-grid gap-3">
            <div class="p-2 bg-light border">Grid item 1</div>
            <div class="p-2 bg-light border">Grid item 2</div>
            <div class="p-2 bg-light border">Grid item 3</div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    name: 'Ping',
    data() {
        return {
        msg: '',
        };
    },
    methods: {
        getMessage() {
            const path = 'http://127.0.0.1:5000/get_indicators';
            axios.get(path)
                .then((res) => {
                this.msg = res.data;
                })
                .catch((error) => {
                console.error(error);
                });
        },
    },
    created() {
        this.getMessage();
    },
};
</script>