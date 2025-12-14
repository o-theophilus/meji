<script>
	import { module, loading, notify, app } from '$lib/store.svelte.js';

	import { IG } from '$lib/input';
	import { Button } from '$lib/button';
	import { Form } from '$lib/layout';
	import { Import } from 'lucide';
	import Value from './variation/value.svelte';

	let item = { ...module.value };
	let form = $state({
		key: item.key,
		quantity: 1,
		variation: {}
	});
	let error = $state({});

	const validate = () => {
		error = {};
		if (form.quantity && (!Number.isInteger(form.quantity) || form.quantity < 1)) {
			error.quantity = 'Please enter a valid number';
		}

		for (const key of Object.keys(item.variation)) {
			if (!form.variation[key] || !item.variation[key].includes(form.variation[key])) {
				error[key] = `Select a ${key}`;
			}
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('Adding item to cart . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/cart`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify(form)
		});
		resp = await resp.json();
		console.log(resp);

		loading.close();

		if (resp.status == 200) {
			notify.open('Item added to cart');
			module.close();
		} else {
			error = resp;
		}
	};
</script>

<Form title="Add to Cart" description="Select variation" error={error.error}>
	{#each Object.entries(item.variation) as [key, values]}
		<IG name={key} error={error[key]}>
			{#snippet input()}
				<div class="line">
					{#each values as value}
						<Value
							active={form.variation[key] == value}
							{value}
							onclick={() => {
								form.variation[key] = value;
							}}
						></Value>
					{/each}
				</div>
			{/snippet}
		</IG>
	{/each}

	<IG name="Quantity" error={error.quantity} type="number" bind:value={form.quantity} />

	<Button icon="cart" onclick={validate}>Add to Cart</Button>
</Form>

<style>
</style>
