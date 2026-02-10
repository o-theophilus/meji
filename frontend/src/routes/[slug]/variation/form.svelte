<script>
	import { Button } from '$lib/button';
	import { Form } from '$lib/layout';
	import { app, loading, module, notify } from '$lib/store.svelte.js';
	import Add from './form.add.svelte';
	import Mod from './form.mod.svelte';

	let ops = $state({
		error: {},
		key: '',
		value: '',
		variation: { ...module.value.variation }
	});

	const reset = () => {
		ops.variation = { ...module.value.variation };
	};

	const submit = async () => {
		ops.error = {};

		if (JSON.stringify(ops.variation) == JSON.stringify(module.value.variation)) {
			ops.error.error = 'No changes were made';
			return;
		}

		loading.open('Saving Post . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/item/${module.value.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify({ variation: ops.variation })
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			module.value.update(resp.item);
			module.close();
			notify.open('Variation Saved');
		} else {
			ops.error = resp;
		}
	};
</script>

<Form title="Edit Variation" error={ops.error.error}>
	<Add bind:ops />
	<Mod bind:ops />

	<div class="line">
		<Button
			icon2="save"
			onclick={submit}
			disabled={JSON.stringify(ops.variation) === JSON.stringify(module.value.variation)}
		>
			Save</Button
		>
		<Button
			icon="history"
			onclick={reset}
			disabled={JSON.stringify(ops.variation) === JSON.stringify(module.value.variation)}
		>
			Reset
		</Button>
	</div>
</Form>
