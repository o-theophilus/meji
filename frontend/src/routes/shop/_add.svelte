<script>
	import { goto } from '$app/navigation';

	import { module, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from '$lib/form.svelte';
	import Button from '$lib/button/button.svelte';
	import IG from '$lib/input_group.svelte';

	let form = {};
	let error = {};

	const validate = async () => {
		error = {};

		if (!form.name) {
			error.name = 'this field is required';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = 'adding . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/item`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(form)
		});
		resp = await resp.json();

		if (resp.status == 200) {
			$module = '';
			goto(`/${resp.item.slug}?edit=true`);
		} else {
			$loading = false;
			error = resp.message;
		}
	};
</script>

<Form>
	<svelte:fragment slot="title">
		<b class="title">Add Item</b>
		Add a new item
	</svelte:fragment>

	<IG name="name" {error} bind:value={form.name} type="text" placeholder="Name here" />

	{#if error.error}
		<p class="error">
			{error.error}
		</p>
		<br />
	{/if}

	<Button primary on:click={validate}>Add</Button>
</Form>
