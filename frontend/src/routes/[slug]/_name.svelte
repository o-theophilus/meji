<script>
	import { module, loading, portal } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from '$lib/form.svelte';
	import Button from '$lib/button.svelte';
	import Info from '$lib/info.svelte';
	import IG from '$lib/input_group.svelte';

	let { item } = $module;
	let error = {};

	const validate = async () => {
		error = {};

		if (!item.name) {
			error.name = 'this field is required';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = true;
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/item/${item.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ name: item.name })
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			if (item.slug != resp.item.slug) {
				window.history.replaceState(history.state, '', `/${resp.item.slug}`);
			}

			$portal = resp.item;

			$module = {
				module: Info,
				status: 200,
				title: '# Details Changed',
				message: 'item name has been changed successfully',
				button: [
					{
						name: 'Ok',
						icon: 'ok',
						fn: () => {
							$module = '';
						}
					}
				]
			};
		} else {
			error = resp;
		}
	};
</script>

<Form>
	<svelte:fragment slot="title">
		<b>Edit Name</b>
	</svelte:fragment>

	<IG name="name" {error} let:id>
		<input bind:value={item.name} {id} type="text" placeholder="Name here" />
	</IG>
	{#if error.error}
		<p class="error">
			{error.error}
		</p>
		<br />
	{/if}
	<Button class="primary" name="Submit" on:click={validate} />
</Form>
