<script>
	import { Form } from '$lib/layout';
	import { module } from '$lib/store.svelte.js';

	import Add from './file.add.svelte';
	import Mod from './file.mod.svelte';

	let blog = $state(module.value.blog);

	let ops = $state({
		key: blog.key,
		files: blog.files,
		title: blog.title,

		count: blog.content.split('@[file]').length - 1,
		active: blog.files[0] || '/no_photo.png',
		error: {}
	});

	let add;
</script>

<Form title="Manage File" error={ops.error.error}>
	<Add bind:ops bind:this={add} />
	<Mod bind:ops onadd={() => add.add()} />
</Form>
