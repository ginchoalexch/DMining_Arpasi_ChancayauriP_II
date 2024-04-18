import React from "react";
import { BentoGrid} from "../components/ui/bento-grid";
import {
  IconArrowWaveRightUp,
  IconBoxAlignRightFilled,
  IconBoxAlignTopLeft,
  IconClipboardCopy,
  IconFileBroken,
  IconSignature,
  IconTableColumn,
} from "@tabler/icons-react";

export function Bentodemo() {
  const handleUploadExcel = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files ? e.target.files[0] : null;
    if (file) {
      // Aquí puedes agregar la lógica para manejar la subida del archivo Excel
      console.log("Archivo Excel subido:", file);
    }
  };

  const items = [
    {
      title: "aca iran las tablas",
      icon: <IconClipboardCopy className="h-4 w-4 text-neutral-500" />,
      action: null,
    },
    {
      title: "aca ira el boton para el excel",
      description: "suba su archivo excel",
      icon: <IconFileBroken className="h-4 w-4 text-neutral-500" />,
      action: (
        <label className="block">
          <input
            type="file"
            accept=".xlsx,.xls"
            className="hidden"
            onChange={handleUploadExcel}
          />
          <button className="w-full py-2 px-4 rounded-md bg-blue-500 text-white hover:bg-blue-600">
            Upload Excel File
          </button>
        </label>
      ),
    },

     
  {
    title: "aca ira el grafico",
    description: "primer grafico",
 
    icon: <IconSignature className="h-4 w-4 text-neutral-500" />,
    action:  <label className="block">
    <input
      type="file"
      accept=".xlsx,.xls"
      className="hidden"
      onChange={handleUploadExcel}
    />
    <button className="w-full py-2 px-4 rounded-md bg-blue-500 text-white hover:bg-blue-600">
      Upload Excel File
    </button>
  </label>
  },
  {
    title: "The Power of Communication",
    description:
      "Understand the impact of effective communication in our lives.",
   
    icon: <IconTableColumn className="h-4 w-4 text-neutral-500" />,
    action: null,
  },
  {
    title: "The Pursuit of Knowledge",
    description: "Join the quest for understanding and enlightenment.",
   
    icon: <IconArrowWaveRightUp className="h-4 w-4 text-neutral-500" />,
    action: null,
  },
  {
    title: "The Joy of Creation",
    description: "Experience the thrill of bringing ideas to life.",
 
    icon: <IconBoxAlignTopLeft className="h-4 w-4 text-neutral-500" />,
    action: null,
  },
  {
    title: "The Spirit of Adventure",
    description: "Embark on exciting journeys and thrilling discoveries.",
    //header: <Skeleton />,
    icon: <IconBoxAlignRightFilled className="h-4 w-4 text-neutral-500" />,
    action: null,
  },
];

return (
  <BentoGrid className="max-w-4xl mx-auto">
    {items.map((item, i) => (
      <BentoGridItem
        key={i}
        title={item.title}
        description={item.description}
        icon={item.icon}
        action={item.action} // Asegúrate de pasar la acción
        className={i === 3 || i === 6 ? "md:col-span-2" : ""}
      />
    ))}
  </BentoGrid>
);
}

const BentoGridItem = ({
  className,
  title,
  description,
  header,
  icon,
  action,
}: {
  className?: string;
  title?: string | React.ReactNode;
  description?: string | React.ReactNode;
  header?: React.ReactNode;
  icon?: React.ReactNode;
  action?: React.ReactNode; // Agrega el prop action
}) => {
  return (
    <div
      className={`row-span-1 rounded-xl group/bento hover:shadow-xl transition duration-200 shadow-input dark:shadow-none p-4 dark:bg-black dark:border-white/[0.2] bg-white border border-transparent justify-between flex flex-col space-y-4 ${className}`}
    >
      {header}
      <div className="group-hover/bento:translate-x-2 transition duration-200">
        {icon}
        <div className="font-sans font-bold text-neutral-600 dark:text-neutral-200 mb-2 mt-2">
          {title}
        </div>
        <div className="font-sans font-normal text-neutral-600 text-xs dark:text-neutral-300">
          {description}
        </div>
        {className === "md:col-span-2" }
      </div>
    </div>
  );
};
