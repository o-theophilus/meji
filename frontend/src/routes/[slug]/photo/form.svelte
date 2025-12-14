<script>
	import { module } from '$lib/store.svelte.js';
	import { Form } from '$lib/layout';

	import Add from './form.add.svelte';
	import Mod from './form.mod.svelte';
	import Module from '$lib/+layout/module.svelte';

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
