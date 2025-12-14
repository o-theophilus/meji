<script>
	import { IG } from '$lib/input';
	import { Button } from '$lib/button';

	let { ops = $bindable() } = $props();
	let value = $derived(
		ops.value
			.replace(/\r?\n/g, ',')
			.replace(/\s+/g, ' ')
			.toLowerCase()
			.split(',')
			.map((i) => i.trim())
			.filter(Boolean)
			.filter((v, i, arr) => arr.indexOf(v) === i)
	);

	const add = () => {
		ops.error = {};

		if (!ops.key) {
			ops.error.key = 'Key is required';
		}
		if (!value.length) {
			ops.error.value = 'Value is required';
		}

		if (Object.keys(ops.error).length != 0) return;

		ops.variation[ops.key] = value;
		ops.key = '';
		ops.value = '';
	};
</script>

<IG name="Name" bind:value={ops.key} error={ops.error.key} type="text" placeholder="Name here" />
<IG
	name="Values"
	bind:value={ops.value}
	error={ops.error.value}
	type="text"
	placeholder="Values here"
	onblur={() => (ops.value = value.join(', '))}
/>
<Button icon="plus" onclick={add}>Add</Button>
