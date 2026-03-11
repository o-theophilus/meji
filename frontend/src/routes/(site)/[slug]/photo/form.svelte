<script>
	import { Form } from '$lib/layout';
	import { module } from '$lib/store.svelte.js';

	import Add from './form.add.svelte';
	import Mod from './form.mod.svelte';

	let item = $state(module.value);

	let ops = $state({
		key: item.key,
		name: item.name,
		files: item.files,

		active: item.files[0] || '/no_photo.png',
		error: {}
	});
</script>

<Form title="Manage File" error={ops.error.error}>
	<Add bind:ops />
	<Mod bind:ops />
</Form>
