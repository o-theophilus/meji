<script>
	import { page } from '$app/stores';
	import Button from '$lib/comp/button.svelte';

	export let item;

	let text = `
	Hi
	%0A
	I want to make enquiry concerning ${item.name} on Meji.ng

	`;
</script>

<Button
	name="Chat"
	icon="whatsapp"
	href="https://api.whatsapp.com/send?phone=+2348067397793&text={text}%20{$page.url.href}"
	target="_blank"
/>
