<script>
	import { page } from '$app/stores';

	export let title;
	export let description;
	export let image = `${$page.url.origin}/favicon.png`;

	title = `${title} | Meji`;
	description = description ? description : title;
</script>

<svelte:head>
	<title>{title}</title>
	<meta name="title" content={title} />
	<meta property="og:title" content={title} />
	<meta property="twitter:title" content={title} />

	<meta name="description" content={description} />
	<meta property="og:description" content={description} />
	<meta property="twitter:description" content={description} />

	<meta property="og:image" content={image} />
	<meta property="twitter:image" content={image} />

	<meta property="og:image:alt" content={title} />
	<meta property="twitter:image:alt" content={title} />

	<meta property="og:url" content={$page.url.href} />
	<meta property="twitter:url" content={$page.url.href} />

	<meta property="og:type" content="website" />
	<meta property="twitter:card" content="summary_large_image" />
</svelte:head>
