<script>
	import { goto } from '$app/navigation';
	import { page } from '$app/state';
	import { Button } from '$lib/button';
	import { Dialogue } from '$lib/info';
	import { IG } from '$lib/input';
	import { Form } from '$lib/layout';
	import { app, loading, module } from '$lib/store.svelte.js';
	let form = $state({});
	let error = $state({});

	const validate = () => {
		error = {};
		if (!form.name) {
			error.name = 'This field is required';
		} else if (form.name.length > 100) {
			error.name = 'This field cannot exceed 100 characters';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('Creating Item . . .');

		let response = await fetch(`${import.meta.env.VITE_BACKEND}/items${page.url.search}`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify(form)
		});
		let result = await response.json();
		loading.close();

		if (response.status == 200) {
			module.value.update(result.items, result.total_page);
			module.open(Dialogue, {
				message: 'Item Created',
				buttons: [
					{
						name: 'OK',
						icon: 'check',
						fn: () => {
							goto(`/${result.item.slug}?edit`);
							module.close();
						}
					}
				]
			});
		} else {
			error = result;
		}
	};
</script>

<Form
	title="Add New Item"
	description="Enter the item name to create a draft. You'll be taken to the item page to add details and images."
	error={error.error}
>
	<IG
		name="Name"
		icon="square-pen"
		error={error.name}
		placeholder="Name here"
		type="text"
		bind:value={form.name}
	/>

	<Button icon2="plus" onclick={validate}>Create Draft & Continue</Button>
</Form>
