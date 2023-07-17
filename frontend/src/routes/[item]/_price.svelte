<script>
	import { module, portal, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from '$lib/module/form.svelte';
	import Button from '$lib/button.svelte';
	import IG from '$lib/input_group.svelte';
	import Info from '$lib/module/info.svelte';

	let { item } = $module;
	let error = {};

	const validate = async () => {
		error = {};

		if (item.price && (!Number.isFinite(item.price) || item.price < 0)) {
			error.price = 'please enter a valid price';
		}

		if (item.old_price) {
			if (!Number.isFinite(item.old_price) || item.old_price < 0) {
				error.old_price = 'please enter a valid price';
			} else if (item.old_price <= item.price) {
				error.old_price = 'old price should be greater than price';
			}
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
			body: JSON.stringify({
				price: item.price,
				old_price: item.old_price
			})
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			$portal = resp.item;

			$module = {
				module: Info,
				status: 200,
				title: '# Details Changed',
				message: 'item price has been changed successfully',
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
		<b>Edit Item</b>
	</svelte:fragment>

	<IG name="price" {error} let:id>
		<input bind:value={item.price} {id} type="number" placeholder="Price here" />
	</IG>

	<IG name="old_price" {error} let:id>
		<input bind:value={item.old_price} {id} type="number" placeholder="Old price here" />
	</IG>
	{#if error.error}
		<p class="error">
			{error.error}
		</p>
		<br />
	{/if}
	<Button class="primary" name="Submit" on:click={validate} />
</Form>
