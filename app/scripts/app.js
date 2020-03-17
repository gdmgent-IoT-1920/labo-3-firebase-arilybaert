const dbConfig = {
    collection: 'raspberry_collection',
    document: 'lectorpi_doc'
};

const app = {
    init() {
        // initialiseer de firebase app
        firebase.initializeApp(firebaseConfig);
        this._db = firebase.firestore();
        // cache the DOM
        this.cacheDOMElements();
        this.cacheDOMEvents();

        this._matrix = {
            isOn: false, color: {value: '#000000', type: 'hex'}
        };
    },
    cacheDOMElements() {
        this.$colorPicker = document.querySelector('#colorPicker');
        this.$toggleMatrix = document.querySelector('#toggleMatrix');
        this.$btnChange = document.querySelector('#btnChange');
    },
    cacheDOMEvents() {
        this.$btnChange.addEventListener('click', (e) => {
            e.preventDefault();
            this._matrix.color.value = this.$colorPicker.value;
            this._matrix.isOn = this.$toggleMatrix.checked;

            this.updateInFirebase();
        });
    },
    updateInFirebase() {
        this._db.collection(dbConfig.collection).doc(dbConfig.document)
            .set(
                {matrix: this._matrix},
                {merge: true}
            );
    }
}

app.init();